from django.contrib import admin, messages

from .models import Area, AreaMap, DataMap, AreaBin


class AreaAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "area_type")


class AreaMapAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "data_source", "dataset_identifier", "created_time")


class DataMapAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "area_map", "data_source", "dataset_identifier", "created_time")

    actions = ["generate_kmlmap_async"]


class AreaBinAdmin(admin.ModelAdmin):

    list_display = ("id", "data_map", "area", "value", "count")


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaMap, AreaMapAdmin)
admin.site.register(DataMap, DataMapAdmin)
admin.site.register(AreaBin, AreaBinAdmin)
