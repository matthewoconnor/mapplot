from django.db import models

AREA_TYPES = (
	("UNCATEGORIZED", "Uncategorized"),
	("N", "Neighborhood"),
	("WARD", "Ward"),
	("STATE", "State"),
	("COUNTRY", "Country"),
	("REGION", "Region"),
	("COUNTY", "County"),
)

BOUNDARY_TYPES = (
	("OUTER", "Outer Boundary"),
	("INNER", "Inner Boundary")
)

class Area(models.Model):
	"""
	A single enclosed area
	"""
	name = models.CharField()
	external_identifier = models.CharField()
	area_type = models.CharField(choices=AREA_TYPES)
	boundary_type = models.CharField(choices=BOUNDARY_TYPES)
	polygon = models.TextField()
	mbr = models.CharField() #n,e,s,w
	outer_area = models.ForeignKey("Area", related_name="inner_area", null=True, blank=True)

	created_time = models.DateTimeField()

	def mbr_from_polygon(self):
		""" code to get minimum bounding rectangle from polygon"""
		pass


class AreaMap(models.Model):
	""" A collection of areas (e.g. Chicago Neighborhoods)"""
	name = models.CharField()
	areas = models.ManyToManyField("Area")
	kml_file = modes.FileField()

	created_time = models.DateTimeField()

	@classmethod
	def import_from_kml(cls, file):
		"""write code to import from kml file using beautiful soup"""
		pass


class KmlMap(models.Model):
	""" A generated KML file for a data map"""
	name = models.CharField()
	user = models.ForeignKey("auth.User")
	polygon = models.TextField()
	kml_file = modes.FileField()

	created_time = models.DateTimeField()



