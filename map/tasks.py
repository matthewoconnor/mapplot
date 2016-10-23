from __future__ import absolute_import

from celery import task, shared_task, chord
from celery.utils.log import get_task_logger
from django_cereal.pickle import DJANGO_CEREAL_PICKLE

logger = get_task_logger(__name__)

@shared_task(name="get_kmlmap_areabins", serializer=DJANGO_CEREAL_PICKLE)
def get_kmlmap_areabins(kmlmap, options=dict()):
	return kmlmap.area_bins_from_soda_dataset(**options)

@shared_task(name="merge_area_bins", serializer=DJANGO_CEREAL_PICKLE)
def merge_area_bins(area_bins, kmlmap):
	return kmlmap.area_bins_from_soda_dataset(**options)

@shared_task(name="generate_kmlmap", serializer=DJANGO_CEREAL_PICKLE)
def generate_kmlmap(kmlmap, search_options=dict()):

	# determine number of concurrent tasks, and options
	client = Socrata(kmlmap.data_source, None)
	search_kwargs = search_options.get("search_kwargs", dict())
	limit = search_options.get("limit", 1000)
	tasks = 4 
	dataset_count = client.get(select="count(id)")[0].get("count_id")
	iterations = math.ceil(count / (cores * limit))

	# run concurrent tasks, only supported by python 3.5
	area_bins = chord(
		get_kmlmap_areabins.s(kmlmap, options={**search_options, **dict(limit=limit, iterations=iterations, offset=i*iterations*limit)}) for i in range(tasks)
	)(merge_area_bins.s(kmlmap)).get()

	# generate file from area bins
	kmlfile_path = kmlmap.save_kmlfile_from_area_bins(area_bins)






