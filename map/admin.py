from django.contrib import admin

from .models import Area, AreaMap, KmlMap

admin.site.register(Area)
admin.site.register(AreaMap)
admin.site.register(KmlMap)
