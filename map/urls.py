from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^(|/)$', views.KmlViewerView.as_view(), name='index'),
    url(r'^kmlmap/create/$', views.KmlmapEdit.as_view(), name="kmlmap_create"),

    url(r'^app/$', TemplateView.as_view(template_name="map/app.html"), name="app"),
    url(r'^app/kmlmap/edit/$', views.KmlMapListJson.as_view(), name="kmlmap_list_json"),
   	url(r'^kmlmap/list/json/$', views.KmlMapListJson.as_view(), name="kmlmap_list_json"),

]