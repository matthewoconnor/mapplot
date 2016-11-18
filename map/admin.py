from django.contrib import admin, messages

from .utils import start_kmlmap_task
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
			task_kwargs = dict()
			task_ids = start_kmlmap_task(kmlmap, **task_kwargs)
			messages.success(request, "Started data import for %s" % kmlmap.name)
			print(task_ids)


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaMap, AreaMapAdmin)
admin.site.register(KmlMap, KmlMapAdmin)
