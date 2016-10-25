from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from .models import KmlMap
from .forms import KmlmapForm


class KmlViewerView(TemplateView):
	""" TempateView with world map and application to view kml maps"""

	template_name = "map/kmlmap-viewer.html"

	def get(self, request, *args, **kwargs):
		self.kmlmaps = KmlMap.objects.all()
		return super().get(request, *args, **kwargs)

class KmlmapEdit(FormView):

	template_name = ""
	form_class = KmlmapForm
