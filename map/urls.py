from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [

    # - Main application
    # - Getting list of DataMaps
    # - Getting DataMap to display
    # - Creating DataMap
    # - Autocomplete AreaMap
    # - Get metadata for DataMap

    url(r'^app/$',
        TemplateView.as_view(template_name="map/app.html"), name="app"),
    url(r'^app/kmlmap/create/$',
        views.KmlmapCreateViewPart.as_view(), name="kmlmap_edit"),
    url(r'^app/kmlmap/(?P<datamap_id>\d+)/metadata/$',
        views.SocrataDatamapMetadata.as_view(), name="kmlmap_metadata"),
    url(r'^app/task/progress/$',
        views.TaskProgressView.as_view(), name="task_progress"),
    url(r'^app/areamap/autocomplete/$',
        views.KmlAreaMapAutocomplete.as_view(), name="areamap_autocomplete"),

    url(r'^kmlmap/list/json/$',
        views.DataMapListJson.as_view(), name="kmlmap_list_json"),

    url(r'^app/datamap/create/$',
        views.DataMapCreateView.as_view(), name="datamap_create"),
    url(r'^app/datamap/import-settings/$',
        views.DataMapImportSettingsView.as_view(), name="datamap_import_settings"),

]