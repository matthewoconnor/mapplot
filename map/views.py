from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from django.http import JsonResponse

from .models import KmlMap, AreaMap
from .tasks import poll_task_progress
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

# create kml area map

class KmlmapCreateViewPart(FormView):
	template_name = "map/app/kmlmap-edit.html"
	form_class = KmlmapForm

class KmlMapListJson(View):

	def get(self, request, *args, **kwargs):
		kmlmaps = KmlMap.objects.all();
		context = dict(
			kmlfiles=[dict(title=km.name, source=km.kml_file.url) for km in kmlmaps]
		)
		return JsonResponse( context )

class TaskProgressView(View):

	def get(self, request, *args, **kwargs):
		task_ids = request.GET.get("task_ids", None)
		task_id_list = task_ids.split(",") if task_ids else []
		context = poll_task_progress(task_id_list)
		return JsonResponse( context )

class KmlAreaMapAutocomplete(View):

	def get(self, request, *args, **kwargs):
		request.GET.get("query", None)
		if query:
			results = AreaMap.objects.filter(name__icontains=query).order_by("name").values("id", "name")
		else:
			results = []
		context = dict(success=True, results=results, query=query)
		return JsonResponse( context )