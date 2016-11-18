from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from django.http import JsonResponse

from .models import KmlMap, AreaMap
from .utils import start_kmlmap_task
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
	template_name = "map/app/kmlmap-form.html"
	form_class = KmlmapForm

	def post(self, request, *args, **kwargs):
		print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		for key, value in request.POST.items():
			print(key, value)
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		kmlmap = form.save()

		task_kwargs = dict(
			where=form.cleaned_data.get("where"),
			limit=form.cleaned_data.get("limit"),
			categorize_method=form.cleaned_data.get("categorize_method"), # latlng, point, match
			lat_field=form.cleaned_data.get("lat_field"),
			lng_field=form.cleaned_data.get("lng_field"),
			point_field=form.cleaned_data.get("point_field"),
			match_soda_field=form.cleaned_data.get("match_soda_field"),
			match_area_field=form.cleaned_data.get("match_area_field")
		)

		print("")
		print(kmlmap.area_map)
		print("")
		print(task_kwargs)
		print("")

		task_ids = start_kmlmap_task(kmlmap, **task_kwargs)

		response_context = dict(success=True, kmlmap=dict(title=kmlmap.name), task_ids=task_ids)

		return JsonResponse(response_context)

	def form_invalid(self, form):
		#print(form.__dir__())
		response_context = dict(success=False, messages=form.errors)
		return JsonResponse(response_context)

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
		print(task_id_list)
		context = poll_task_progress(task_id_list)
		return JsonResponse( context )

class KmlAreaMapAutocomplete(View):

	def get(self, request, *args, **kwargs):
		query = request.GET.get("query", None)
		if query:
			results = AreaMap.objects.filter(name__icontains=query).order_by("name").values("id", "name")
		else:
			results = []
		context = dict(success=True, results=list(results), query=query)
		return JsonResponse( context )




