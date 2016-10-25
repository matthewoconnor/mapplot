from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^(|/)$', views.KmlViewerView.as_view(), name='index'),
    url(r'^kmlmap/create/$', views.KmlmapEdit.as_view(), name="kmlmap_create")
]