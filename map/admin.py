from django.contrib import admin, messages

from .tasks import import_areas_from_kml_file
from .models import Area, AreaMap, DataMap, AreaBin


class AreaAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "area_type")


class AreaMapAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "data_source", "dataset_identifier", "created_time")

    actions = ["generate_areas_from_kmlfile"]

    def generate_areas_from_kmlfile(modeladmin, request, queryset):
    	for areamap in queryset:
    		import_areas_from_kml_file.apply_async(args=[areamap])


class DataMapAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "area_map", "data_source", "dataset_identifier", "created_time")


class AreaBinAdmin(admin.ModelAdmin):

    list_display = ("id", "data_map", "area", "value", "count")


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaMap, AreaMapAdmin)
admin.site.register(DataMap, DataMapAdmin)
admin.site.register(AreaBin, AreaBinAdmin)
