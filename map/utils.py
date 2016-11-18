def kml_hex_color_from_value_range(value, the_min, the_max):

	range_size = the_max - the_min
	norm_range_size = 256
	half_norm_range_size = norm_range_size/2
	norm_value = (((value - the_min) * norm_range_size) / range_size)

	blue  = "{:02x}".format( int(max(half_norm_range_size - norm_value, 0)) )
	green = "{:02x}".format( int(half_norm_range_size - abs(norm_value - half_norm_range_size)) )
	red   = "{:02x}".format( int(max(norm_value - half_norm_range_size, 0)) )

	opacity = "ee"

	return "{oo}{bb}{gg}{rr}".format(oo=opacity, bb=blue, gg=green, rr=red)


def kml_height_from_value_range(value, the_min, the_max):

	range_size = the_max - the_min

	the_norm_min = 100
	the_norm_max = 5000
	norm_range_size = the_norm_max - the_norm_min

	return (((value - the_min) * norm_range_size) / range_size) + the_norm_min

def start_kmlmap_task(kmlmap, **kwargs):

	limit = kwargs.get("limit", 1000);
	search_kwargs = kwargs.get("search_kwargs", dict());
	lat_field = kwargs.get("lat_field", "latitude");
	lng_field = kwargs.get("lng_field", "longitude");

	client = kmlmap.get_socrata_client()

	tasks = 4

	dataset_count = client.get(kmlmap.dataset_identifier, exclude_system_fields=False, select="count(:id)")[0].get("count_id", **search_kwargs)
	limit = min(limit, math.ceil( int(dataset_count)/tasks) )
	iterations = math.ceil(int(dataset_count) / (tasks * limit))

	get_bins_group = [get_kmlmap_areabins_2.si(kmlmap, {**search_kwargs, **dict(limit=limit, iterations=iterations, offset=i*iterations*limit)}) for i in range(tasks)]

	workflow = chord(get_bins_group, merge_area_bins_2.s(kmlmap))
	asyn_result = workflow.apply_async()

	progress_task_ids = [ar.task_id for ar in asyn_result.parent.children]
	return progress_task_ids