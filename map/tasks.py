from __future__ import absolute_import

from celery import task, shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from django_cereal.pickle import DJANGO_CEREAL_PICKLE

logger = get_task_logger(__name__)

@shared_task(name="get_kmlmap_areabins", serializer=DJANGO_CEREAL_PICKLE)
def get_kmlmap_areabins(kmlmap, options=dict()):
    return kmlmap.area_bins_from_soda_dataset(**options)

@shared_task(name="merge_area_bins", serializer=DJANGO_CEREAL_PICKLE)
def merge_area_bins(area_bins_list, kmlmap):
    merged_bins = []
    for area_bin in (item for sublist in area_bins_list for item in sublist):
        merged_bin = next((ab for ab in merged_bins if ab["area"] == area_bin["area"]), None)
        if not merged_bin:
            merged_bins.append(area_bin)
        else:
            merged_bin["count"] += area_bin["count"]
    return merged_bins

@shared_task(name="generate_kmlmap", serializer=DJANGO_CEREAL_PICKLE)
def generate_kmlmap(area_bins, kmlmap):
    return kmlmap.save_kmlfile_from_area_bins(area_bins)

@shared_task(name="blank_task", serializer=DJANGO_CEREAL_PICKLE)
def blank_task(name="No Name"):
    # use at front of chain if followed by a group
    return name


@shared_task(name="add", serializer=DJANGO_CEREAL_PICKLE)
def add(x, y):
    return x + y

@shared_task(name="tsum", serializer=DJANGO_CEREAL_PICKLE)
def tsum(numbers):
    return sum(numbers)


# TESTING PROGRESS STATUS
@shared_task(name="get_kmlmap_areabins_2", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def get_kmlmap_areabins_2(self, kmlmap, **kwargs):
    limit = kwargs.get("limit", 1000)
    offset = kwargs.get("offset", 0)
    iterations = kwargs.get("iterations", 1)
    search_kwargs = kwargs.get("search_kwargs", dict())
    lng_fieldname = kwargs.get("lng_field", "longitude")
    lat_fieldname = kwargs.get("lat_field", "latitude")

    client = kmlmap.get_socrata_client()

    areas = kmlmap.area_map.areas.filter(
        is_primary=True
    ).prefetch_related("inner_areas", "child_areas__inner_areas")

    area_bins = [dict(
            area=area,
            polygons=area.get_grouped_polygon_list(),
            count=0,
        ) for area in areas]

    i = 0
    without_coords = 0

    self.update_state(state='PROGRESS', meta={'current': i, 'total': iterations}) # initial progress state

    while i < iterations:

        i += 1

        self.update_state(state='PROGRESS', meta={'current': i, 'total': iterations}) # update as we go

        data = client.get(
            kmlmap.dataset_identifier, 
            content_type="json", 
            limit=limit, 
            offset=offset, **search_kwargs)

        if not data:
            print("done with data")
            break
        else:
            print("data {0} to {1}".format(offset, offset + limit))

        for row in data:

            try:
                lat_value = row[lat_fieldname]
                lng_value = row[lng_fieldname]
                if isinstance(lat_value, dict) and lat_value.get("type", "") == "Point":
                    coords = lat_value.get("coordinates")
                    lng = float(coords[0])
                    lat = float(coords[1])
                else:
                    lng = float(lng_value)
                    lat = float(lat_value)

                for ab in area_bins:
                    if ab["area"].group_contains_point(lng, lat, grouped_polygon_list=ab["polygons"]):
                        ab["count"] += 1
                        break
            except:
                without_coords += 1

        offset += limit

    return area_bins

@shared_task(name="merge_area_bins_2", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def merge_area_bins_2(self, area_bins_list, kmlmap):
    area_bins = [item for sublist in area_bins_list for item in sublist]
    TOTAL = len(area_bins)
    merged_bins = []

    for i, area_bin in enumerate(area_bins):
        self.update_state(state='PROGRESS', meta={'current': i, 'total': TOTAL}) # tracking progress
        merged_bin = next((ab for ab in merged_bins if ab["area"] == area_bin["area"]), None)
        if not merged_bin:
            merged_bins.append(area_bin)
        else:
            merged_bin["count"] += area_bin["count"]
    logger.info("ABOUT TO SAVE FILE!!!")
    return kmlmap.save_kmlfile_from_area_bins(merged_bins)

def poll_task_progress(task_id_list):
    # assumes all tasks are equal length

    fraction_complete = 0.0
    has_started = False # assume not
    is_complete = True # assume it is
    task_total = len(task_id_list)

    for task_id in task_id_list:
        try:
            task = AsyncResult(task_id)
            state = task.state

            print("TASK STATE", state)

            if state in ["SUCCESS", "FAILURE", "REVOKED"]:
                has_started = True
                fraction_complete += (1.0/task_total)
            elif state == "PROGRESS" and task.result:
                has_started = True
                is_complete = False
                total = task.result.get("total", 1)
                current = task.result.get("current", 1)
                fraction_complete += (current/total)/task_total
            else:
                is_complete = False
        except:
            is_complete = False

    if is_complete:
        status = "COMPLETE"
        fraction_complete = 1.0
    elif has_started:
        status = "PROGRESS"
    else:
        status = "PENDING"

    return dict(
        status=status,
        complete=fraction_complete)














