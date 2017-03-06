import math

from celery import chord

from .tasks import get_kmlmap_areabins, merge_datamap_areabins, get_datamap_areabins


def kml_hex_color_from_value_range(value, the_min, the_max):

    range_size = the_max - the_min
    norm_range_size = 256
    half_norm_range_size = norm_range_size/2
    norm_value = (((value - the_min) * norm_range_size) / range_size)

    blue  = "{:02x}".format( int(max(half_norm_range_size - norm_value, 0)) )
    green = "{:02x}".format( int(half_norm_range_size - abs(norm_value - half_norm_range_size)) )
    red   = "{:02x}".format( int(max(norm_value - half_norm_range_size, 0)) )

    opacity = "ff"

    return "{oo}{bb}{gg}{rr}".format(oo=opacity, bb=blue, gg=green, rr=red)


def kml_height_from_value_range(value, the_min, the_max):

    range_size = the_max - the_min

    the_norm_min = 100
    the_norm_max = 5000
    norm_range_size = the_norm_max - the_norm_min

    return (((value - the_min) * norm_range_size) / range_size) + the_norm_min


# NEW
def start_datamap_import_task(datamap):
    LIMIT = 5000
    TASKS = 4
    client = kmlmap.get_socrata_client()

    dataset_count = datamap.get_dataset_count()
    limit = min(LIMIT, math.ceil(int(dataset_count)/TASKS))
    iterations = math.ceil(int(dataset_count) / (TASKS * limit))

    soda_query_kwargs = dict(limit=limit, iterations=iterations)
    if datamap.querystring:
        soda_query_kwargs["where"] = datamap.querystring

    get_bins_group = [get_datamap_areabins.si(kmlmap, **{
        **soda_query_kwargs,
        **dict(offset=i*iterations*limit)
    }) for i in range(tasks)]

    workflow = chord(get_bins_group, merge_datamap_areabins.s(kmlmap))
    async_result = workflow.apply_async()

    progress_task_ids = [ar.task_id for ar in async_result.parent.children] + [async_result.task_id]
    return progress_task_ids


# OLD
def start_kmlmap_task(kmlmap, **kwargs):

    limit = kwargs.get("limit", 1000);
    where = kwargs.get("where", None);
    lat_field = kwargs.get("lat_field", "latitude");
    lng_field = kwargs.get("lng_field", "longitude");

    client = kmlmap.get_socrata_client()

    tasks = 4

    search_kwargs = dict(where=where) if where else dict()

    dataset_count = client.get(kmlmap.dataset_identifier, exclude_system_fields=False, select="count(:id)", **search_kwargs)[0].get("count_id")
    limit = min(limit, math.ceil( int(dataset_count)/tasks) )
    iterations = math.ceil(int(dataset_count) / (tasks * limit))

    get_bins_group = [get_kmlmap_areabins.si(kmlmap, **{**search_kwargs, **dict(limit=limit, iterations=iterations, offset=i*iterations*limit)} ) for i in range(tasks)]

    workflow = chord(get_bins_group, merge_area_bins.s(kmlmap))
    async_result = workflow.apply_async()

    progress_task_ids = [ar.task_id for ar in async_result.parent.children] + [async_result.task_id]
    return progress_task_ids
