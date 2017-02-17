from __future__ import absolute_import

from celery import task, shared_task
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from django_cereal.pickle import DJANGO_CEREAL_PICKLE

logger = get_task_logger(__name__)

@shared_task(name="blank_task", serializer=DJANGO_CEREAL_PICKLE)
def blank_task(name="No Name"):
    # use at front of chain if followed by a group
    return name

# OLD
@shared_task(name="get_kmlmap_areabins", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def get_kmlmap_areabins(self, kmlmap, **kwargs):

    task = self
    def update_task_progress(i, total):
        task.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    kwargs["on_iteration"] = update_task_progress

    return kmlmap.area_bins_from_soda_dataset(**kwargs)

# OLD
@shared_task(name="merge_area_bins", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def merge_area_bins(self, area_bins_list, kmlmap):

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

    return kmlmap.save_kmlfile_from_area_bins(merged_bins)

# KEEP
@shared_task(name="import_areas_from_kml_file", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def import_areas_from_kml_file(self, areamap, **kwargs):

    the_task = self

    def update_task_progress(i, total):
        the_task.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    kwargs["on_iteration"] = update_task_progress

    areamap.import_areas_from_kml_file(**kwargs)

# NEW
@shared_task(name="get_datamap_areabins", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def get_datamap_areabins(self, datamap, **kwargs):

    the_task = self

    def update_task_progress(i, total):
        the_task.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    kwargs["on_iteration"] = update_task_progress

    return datamap.areabin_dict_from_socrata_dataset(**kwargs)

# NEW
@shared_task(name="merge_area_bins", bind=True, serializer=DJANGO_CEREAL_PICKLE)
def merge_areabins(self, areabins_list, datamap):

    areabins = [item for sublist in areabins_list for item in sublist]
    TOTAL = len(areabins)
    merged_bins = []

    for i, areabin in enumerate(areabins):
        self.update_state(state='PROGRESS', meta={'current': i, 'total': TOTAL}) # tracking progress
        merged_bin = next((ab for ab in merged_bins if ab["area"] == areabin["area"]), None)
        if not merged_bin:
            merged_bins.append(areabin)
        else:
            merged_bin["count"] += areabin["count"]

    return datamap.save_areabins_from_dicts(merged_bins)


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














