from django.contrib import admin

from .models import Area, AreaMap, KmlMap


class AreaAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "area_type")


class AreaMapAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "data_source", "dataset_identifier", "created_time")


class KmlMapAdmin(admin.ModelAdmin):

	list_display = ("id", "name", "area_map", "data_source", "dataset_identifier", "created_time")


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaMap, AreaMapAdmin)
admin.site.register(KmlMap, KmlMapAdmin)
