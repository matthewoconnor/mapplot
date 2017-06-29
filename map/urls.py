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
        views.DataMapApplicationView.as_view(), name="app"),
    
    url(r'^app/task/progress/$',
        views.TaskProgressView.as_view(), name="task_progress"),
    url(r'^app/areamap/autocomplete/$',
        views.KmlAreaMapAutocomplete.as_view(), name="areamap_autocomplete"),

    url(r'^kmlmap/list/json/$',
        views.DataMapListJson.as_view(), name="kmlmap_list_json"),

    url(r'^app/datamap/(?P<datamap_id>\d+)/metadata/$',
        views.SocrataDatamapMetadata.as_view(), name="kmlmap_metadata"),
    url(r'^app/datamap/(?P<datamap_id>\d+)/metadata/columns/',
        views.SocrataDataMapMetaDataColumns.as_view(), name="datamap_metadata_columns"),

    url(r'^app/datamap/create/$',
        views.DataMapCreateView.as_view(), name="datamap_create"),
    url(r'^app/datamap/(?P<datamap_id>\d+)/update/$',
        views.DataMapUpdateView.as_view(), name="datamap_update"),
    url(r'^app/datamap/(?P<datamap_id>\d+)/import-settings/$',
        views.DataMapImportSettingsView.as_view(), name="datamap_import_settings"),

    url(r'^app/datamap/(?P<datamap_id>\d+)/geometry/',
        views.DataMapGeometry.as_view(), name="datamap_geometry"),

    

]