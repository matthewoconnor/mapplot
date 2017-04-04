import re
import requests
import matplotlib.path as matplotlib_path
import numpy as np

from pyquery import PyQuery as pq
from sodapy import Socrata

from django.db import models
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.conf import settings

from .utils import kml_hex_color_from_value_range, kml_height_from_value_range

AREA_TYPES = (
    ("UNCATEGORIZED", "Uncategorized"),
    ("NEIGHBORHOOD", "Neighborhood"),
    ("WARD", "Ward"),
    ("DISTRICT", "District"),
    ("STATE", "State"),
    ("COUNTRY", "Country"),
    ("REGION", "Region"),
    ("COUNTY", "County"),
)

BOUNDARY_TYPES = (
    ("OUTER", "Outer Boundary"),
    ("INNER", "Inner Boundary")
)

WEIGHT_TYPES = (
    ("COUNT", "Count Instances"),
    ("SUM", "Sum Field value")
)

CATEGORIZE_TYPES = (
    ("POINT", "Location Point"),
    ("LATLNG", "Latitude Longitude"),
    ("JOIN", "Join on Common Field"),
    ("JOIN_MAP", "Join on Field Mapping")
)

DATASET_TYPES = (
    ("SOCRATA", "Socrata Soda Data Portal"),
    ("OTHER", "Url for Other Data Source")
)


class Area(models.Model):
    """
    A single enclosed area
    """
    name = models.CharField(max_length=256)
    external_identifier = models.CharField(max_length=256)
    area_type = models.CharField(max_length=64, choices=AREA_TYPES)
    boundary_type = models.CharField(max_length=64, choices=BOUNDARY_TYPES)
    polygon = models.TextField()
    mbr = models.CharField(max_length=256) #n,e,s,w
    is_primary = models.BooleanField(default=True)

    outer_area = models.ForeignKey("Area", related_name="inner_areas", related_query_name="inner_area", null=True, blank=True)
    primary_area = models.ForeignKey("Area", related_name="child_areas", related_query_name="child_area", null=True, blank=True)

    created_time = models.DateTimeField()

    def __str__(self):
        return self.name

    def contains_point(self, lng, lat, polygon_list=None):
        """ tests if a point is within this area
                test for minumum bounding rectangle 
                before trying more expensive contains_point method """
        n, e, s, w = self.mbr.split(",")
        if lng < float(e) and lng > float(w) and lat < float(n) and lat > float(s):
            polygon_list = polygon_list or self.get_polygon_list()
            path = matplotlib_path.Path(np.array(polygon_list))
            return path.contains_point((lng, lat))
        else:
            return False

    def group_contains_point(self, lng, lat, grouped_polygon_list=None):
        """ tests if a point is within this area
                test for minumum bounding rectangle 
                before trying more expensive contains_point method """
        grouped_polygon_list = grouped_polygon_list or self.get_grouped_polygon_list()
        for polygon in grouped_polygon_list:
            if polygon["area"].contains_point(lng, lat, polygon_list=polygon["outer"]):
                is_within_inner_polygon = False # assume contains point until we find point within inner polygon
                for inner_area in polygon["inner"]:
                    if inner_area["area"].contains_point(lng, lat, polygon_list=inner_area["polygon"]):
                        is_within_inner_polygon = True
                        break
                if not is_within_inner_polygon:
                    return True
        return False

    def get_polygon_list(self):
        return [point.split(",") for point in self.polygon.split(";")]

    def get_grouped_polygon_list(self):
        """ meant to be called on the primary area"""
        return [{
                "area":self,
                "outer":self.get_polygon_list(),
                "inner":[dict(area=ia, polygon=ia.get_polygon_list()) for ia in self.inner_areas.all()]
            }] + [{
                "area":ca,
                "outer":ca.get_polygon_list(),
                "inner":[dict(area=ia, polygon=ia.get_polygon_list()) for ia in ca.inner_areas.all()]
            } for ca in self.child_areas.all()]

    def get_geometry(self):
        """Almost identical to get_grouped_polygon_list, but without area instances"""
        return [{
            "outer":self.get_polygon_list(),
            "inner":[ia.get_polygon_list() for ia in self.inner_areas.all()]
        }] + [{
            "outer":ca.get_polygon_list(),
            "inner":[ia.get_polygon_list() for ia in ca.inner_areas.all()]
        } for ca in self.child_areas.all()]

    def mbr_from_polygon(self):
        points = self.polygon.split(";")
        lngs = []
        lats = []
        for point in points:
            coords = point.split(",")
            lngs.append(float(coords[0]))
            lats.append(float(coords[1]))
        return "{n},{e},{s},{w}".format(n=max(lats), e=max(lngs), s=min(lats), w=min(lngs))

    def save(self, *args, **kwargs):
        self.created_time = self.created_time or timezone.now()
        return super().save(*args, **kwargs)


class AreaMap(models.Model):
    """ 
    A collection of areas (e.g. Chicago Neighborhoods)
    """
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)
    areas = models.ManyToManyField("Area", null=True, blank=True)
    data_source = models.CharField(max_length=256, null=True, blank=True) # e.g. "data.cityofchicago.org"
    dataset_identifier = models.CharField(max_length=256, null=True, blank=True)

    kml_file = models.FileField(upload_to="uploads/areamap/", null=True, blank=True)
    area_name_path = models.CharField(max_length=256, null=True, blank=True)
    area_external_identifier_path = models.CharField(max_length=256, null=True, blank=True)
    area_default_type = models.CharField(max_length=64, null=True, blank=True)

    created_time = models.DateTimeField()

    def import_areas_from_kml_file(self, *args, **kwargs):
        
        on_iteration = kwargs.get("on_iteration", None)

        d = pq(filename=self.kml_file.path, parser="xml")
        placemarks = d("Placemark")
        total = len(placemarks)
        i = 0

        # If callable function is passed to keep track of progress, call it
        if on_iteration:
            on_iteration(i, total)

        for placemark in placemarks.items():

            # If callable function is passed to keep track of progress, call it
            i += 1
            if on_iteration:
                on_iteration(i, total)

            polygons = placemark.find("Polygon")
            primary_area = None 

            for polygon in polygons.items():

                outer_boundary_text = polygon.find("outerBoundaryIs LinearRing coordinates").text()
                inner_boundaries = polygon.find("innerBoundaryIs")

                area = Area(
                    polygon=re.sub(r"\s+", ";", outer_boundary_text.strip()),
                    name=placemark.find(self.area_name_path).text(), # e.g. "Data[name='ntaname'] value"
                    external_identifier=placemark.find(self.area_external_identifier_path).text(), # e.g. "Data[name='ntacode'] value"
                    area_type=self.area_default_type,
                    boundary_type="OUTER"
                )

                area.mbr = area.mbr_from_polygon()

                # only one outer area (the primary area) is related to the area map, all others are children
                if primary_area:
                    area.primary_area = primary_area
                    area.is_primary = False
                    area.save()
                else:
                    primary_area = area
                    area.save()
                    self.areas.add(area)

                for inner_boundary in inner_boundaries.items():
                    inner_boundary_text = inner_boundary.find("LinearRing coordinates").text()
                    inner_area = Area(
                        polygon=re.sub(r"\s+", ";", inner_boundary_text.strip()),
                        name="{0} Inner".format(area.name),
                        external_identifier=area.external_identifier,
                        area_type=self.area_default_type,
                        boundary_type="INNER",
                        outer_area=area
                    )

                    inner_area.mbr = inner_area.mbr_from_polygon()
                    inner_area.save()

    @classmethod
    def import_from_geojson(cls, file, *args, **kwargs):
        """write code to import from geojson file"""
        # feature_path = kwargs.get("feature_path",".")
        pass

    def import_areas_from_soda(self, field_mapping, defaults):
        
        # e.g. this is for chicago neighborhoods
        # field_mapping = dict(
        #   polygon="the_geom",
        #   name="community",
        #   external_identifier="area_num_1"
        # )

        # defaults = dict(
        #   area_type="NEIGHBORHOOD",
        # )

        # client = Socrata(self.data_source, "FakeAppToken", username="fakeuser@somedomain.com", password="ndKS92mS01msjJKs")
        client = Socrata(self.data_source, None)
        data = client.get(self.dataset_identifier, content_type="json")

        for area in data:
            coordinates = area[field_mapping["polygon"]]["coordinates"][0][0]
            lngs = []
            lats = []
            polygon = []
            for c in coordinates:
                lngs.append(c[0])
                lats.append(c[1])
                polygon.append( ",".join([str(i) for i in c]) )
            mbr = "{n},{e},{s},{w}".format(n=max(lats), e=max(lngs), s=min(lats), w=min(lngs))

            area_data = dict(
                polygon= ";".join(polygon),
                name=area[field_mapping["name"]],
                external_identifier=area[field_mapping["external_identifier"]],
                mbr=mbr,
                **defaults
            )

            a = Area.objects.create(**area_data)

            self.areas.add(a)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.created_time = self.created_time or timezone.now()
        return super().save(*args, **kwargs)


class AreaBin(models.Model):
    data_map = models.ForeignKey("DataMap")
    area = models.ForeignKey("Area")
    value = models.FloatField(default=0.0) # value of the bin
    count = models.IntegerField(default=0) # number of rows used for bin

    def get_geometry(self):
        return {
            "id": self.id,
            "name": self.area.name,
            "geometry": self.area.get_geometry(),
            "value": self.value,
            "count": self.count
        }


class DataMap(models.Model):
    """
    A generated KML file for a data map
    """
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey("auth.User")

    area_map = models.ForeignKey("AreaMap", null=True, blank=True)

    dataset_type = models.CharField(max_length=256, choices=DATASET_TYPES, blank=True)

    # for socrata datasets
    data_source = models.CharField(max_length=256, null=True, blank=True) # e.g. "data.cityofchicago.org"
    dataset_identifier = models.CharField(max_length=256, null=True, blank=True)

    # other datasets
    dataset_url = models.URLField(max_length=256, blank=True)
    
    weight_type = models.CharField(max_length=64, choices=WEIGHT_TYPES)
    categorize_type = models.CharField(choices=CATEGORIZE_TYPES, max_length=64)

    point_key = models.CharField(max_length=256, blank=True)
    latitude_key = models.CharField(max_length=256, blank=True)
    longitude_key = models.CharField(max_length=256, blank=True)
    join_key = models.CharField(max_length=256, blank=True)
    join_map_file = models.FileField(upload_to="uploads/joinmap/", null=True, blank=True) # json file for complex join mapping

    value_key = models.CharField(max_length=256, blank=True)
    querystring = models.CharField(max_length=256, blank=True)

    kml_file = models.FileField(upload_to="uploads/datamap/", null=True, blank=True)

    task_id = models.CharField(max_length=256, blank=True)  # For tracking progress

    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    # KEEP
    def get_file_url(self):
        try:
            return self.kml_file.url
        except:
            return None

    # KEEP
    def get_socrata_client(self, *args, **kwargs):
        socrata_credentials = settings.DATA_PORTAL_KEYS.get("socrata", None)
        session_adapter = dict(
                prefix="http://", 
                adapter=requests.adapters.HTTPAdapter(max_retries=3))
        if socrata_credentials:
            return Socrata(
                self.data_source, 
                socrata_credentials["app_token"], 
                username=socrata_credentials["username"],
                password=socrata_credentials["password"],
                session_adapter=session_adapter)
        else:
            return Socrata(
                self.data_source, 
                None, 
                session_adapter=session_adapter)

    def get_dataset_count(self, *args, **kwargs):
        # to do: include filters
        client = self.get_socrata_client()
        dataset_count = client.get(self.dataset_identifier, exclude_system_fields=False, select="count(:id)")[0].get("count_id")
        return dataset_count

    # NEW
    def areabin_dict_from_socrata_dataset(self, *args, **kwargs):
        limit = kwargs.get("limit", 1000)
        offset = kwargs.get("offset", 0)
        iterations = kwargs.get("iterations", 1)
        on_iteration = kwargs.get("on_iteration", None)

        client = self.get_socrata_client()

        areas = self.area_map.areas.filter(
            is_primary=True
        ).prefetch_related("inner_areas", "child_areas__inner_areas")

        area_bins = [dict(
            area=area,
            polygons=area.get_grouped_polygon_list(),
            count=0,
        ) for area in areas]

        i = 0

        # If callable function is passed to keep track of progress, call it
        if on_iteration:
            on_iteration(i, iterations)

        while i < iterations:

            i += 1

            # If callable function is passed to keep track of progress, call it
            if on_iteration:
                on_iteration(i, iterations)

            data = client.get(
                self.dataset_identifier,
                content_type="json",
                limit=limit,
                offset=offset) # ADD WHERE CLAUSE FROM QUEYSTRING

            if not data:
                break

            if self.categorize_type == "POINT":
                for row in data:
                    try:
                        point = row[self.point_key]
                        coords = point.get("coordinates")
                        lng = float(coords[0])
                        lat = float(coords[1])
                        for ab in area_bins:
                            if ab["area"].group_contains_point(lng, lat, grouped_polygon_list=ab["polygons"]):
                                ab["count"] += 1
                                break
                    except:
                        pass

            elif self.categorize_type == "LATLNG":
                for row in data:
                    try:
                        lng = float(row[self.latitude_key])
                        lat = float(row[self.longitude_key])
                        for ab in area_bins:
                            if ab["area"].group_contains_point(lng, lat, grouped_polygon_list=ab["polygons"]):
                                ab["count"] += 1
                                break
                    except:
                        pass

            offset += limit

        return area_bins

    # KEEP
    def save_kmlfile_from_areabins(self):
        areabins = self.areabins.all()
        counts = [ab.count for ab in areabins]
        min_count = min(counts)
        max_count = max(counts)

        for ab in areabins:
            ab["height"] = kml_height_from_value_range(ab.count, min_count, max_count)
            ab["color"] = kml_hex_color_from_value_range(ab.count, min_count, max_count)

        kml_string = render_to_string("map/map_template.kml", dict(
            kml_map=self,
            areabins=areabins
        ))

        self.kml_file.save("{0} {1}.kml".format(self.name, self.id), ContentFile(kml_string))

        return self.kml_file.path

    # NEW
    def save_areabins_from_dicts(self, areabin_dicts):
        for ab_dict in areabin_dicts:
            AreaBin.objects.update_or_create(
                data_map=self,
                area=ab_dict["area"],
                defaults={
                    "count": ab_dict.get("count", 0),
                    "value": ab_dict.get("value", 0.0)
                });

    def kml_mapplot_from_soda_dataset(self, *args, **kwargs):
        area_bins = self.area_bins_from_soda_dataset(*args, **kwargs)
        return self.save_kmlfile_from_area_bins(area_bins)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.created_time = self.created_time or now
        self.updated_time = now
        self.user_id = 1 # REMOVE WHEN ABILITY FOR MORE USERS
        return super().save(*args, **kwargs)


