def kml_hex_color_from_value_range(value, the_min, the_max):

	range_size = the_max - the_min
	norm_range_size = 256
	half_norm_range_size = norm_range_size/2
	norm_value = (((value - the_min) * norm_range_size) / range_size)

	blue  = "{:02x}".format( int(max(half_norm_range_size - norm_value, 0)) )
	green = "{:02x}".format( int(half_norm_range_size - abs(norm_value - half_norm_range_size)) )
	red   = "{:02x}".format( int(max(norm_value - half_norm_range_size, 0)) )

	opacity = "af"

	return "{oo}{bb}{gg}{rr}".format(oo=opacity, bb=blue, gg=green, rr=red)


def kml_height_from_value_range(value, the_min, the_max):

	range_size = the_max - the_min

	the_norm_min = 100
	the_norm_max = 5000
	norm_range_size = the_norm_max - the_norm_min

	return (((value - the_min) * norm_range_size) / range_size) + the_norm_min


