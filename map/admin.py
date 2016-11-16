import math
from celery import group

from django.contrib import admin, messages

from .tasks import get_kmlmap_areabins, merge_area_bins, generate_kmlmap
from .models import Area, AreaMap, KmlMap


class AreaAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "area_type")


class AreaMapAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "data_source", "dataset_identifier", "created_time")


class KmlMapAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "area_map", "data_source", "dataset_identifier", "created_time")

	actions = ["generate_kmlmap_async"]

	def generate_kmlmap_async(self, request, queryset):

		for kmlmap in queryset:

			client = kmlmap.get_socrata_client()
			limit = 1000
			tasks = 4

			dataset_count = client.get(kmlmap.dataset_identifier, exclude_system_fields=False, select="count(:id)")[0].get("count_id")
			limit = min(limit, math.ceil( int(dataset_count)/tasks) )
			iterations = math.ceil(int(dataset_count) / (tasks * limit))

			get_bins_group = [get_kmlmap_areabins.s(kmlmap, options=dict(limit=limit, iterations=iterations, offset=i*iterations*limit)) for i in range(tasks)]

			workflow = (group(get_bins_group) | merge_area_bins.s(kmlmap) | generate_kmlmap.s(kmlmap) )
			workflow()

			messages.success(request, "Started data import for %s" % kmlmap.name)


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaMap, AreaMapAdmin)
admin.site.register(KmlMap, KmlMapAdmin)
