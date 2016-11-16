from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from django.http import JsonResponse

from .models import KmlMap
from .forms import KmlmapForm


class KmlViewerView(TemplateView):
	""" TempateView with world map and application to view kml maps"""

	template_name = "map/kmlmap-viewer.html"

	def get(self, request, *args, **kwargs):
		self.kmlmaps = KmlMap.objects.all()
		return super().get(request, *args, **kwargs)

class KmlmapEdit(FormView):

	template_name = "map/kmlmap-import-dataset-form.html"
	form_class = KmlmapForm



class KmlmapEditViewPart(FormView):
	template_name = "map/app/kmlmap-edit.html"
	form_class = KmlmapForm

class KmlMapListJson(View):

	def get(self, request, *args, **kwargs):
		kmlmaps = KmlMap.objects.all();
		return JsonResponse( dict(kmlfiles=[dict(title=km.name, source=km.kml_file.url) for km in kmlmaps]) )