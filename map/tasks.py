from __future__ import absolute_import

from celery import task, shared_task
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
	kmlmap.save_kmlfile_from_area_bins(area_bins)


@shared_task(name="add", serializer=DJANGO_CEREAL_PICKLE)
def add(x, y):
	return x + y

@shared_task(name="tsum", serializer=DJANGO_CEREAL_PICKLE)
def tsum(numbers):
    return sum(numbers)



