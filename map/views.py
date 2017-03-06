from django.views.generic import View, FormView
from django.http import JsonResponse

from .models import DataMap, AreaMap
from .utils import start_kmlmap_task, start_datamap_import_task
from .tasks import poll_task_progress
from .forms import KmlmapForm, DataMapImportSettingsForm


class KmlmapCreateViewPart(FormView):
    template_name = "map/app/kmlmap-form.html"
    form_class = KmlmapForm

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

        task_ids = start_kmlmap_task(kmlmap, **task_kwargs)

        response_context = dict(success=True, kmlmap=dict(id=kmlmap.id, title=kmlmap.name), task_ids=task_ids)

        return JsonResponse(response_context)

    def form_invalid(self, form):
        response_context = dict(success=False, messages=form.errors)
        return JsonResponse(response_context)


# NEW DATAMAP CREATE VIEWS
class DataMapCreateView(FormView):
    template_name = "map/app/kmlmap-form.html"
    form_class = KmlmapForm

    def form_valid(self, form):
        datamap = form.save()
        response_context = dict(success=True, datamap=datamap)
        return JsonResponse(response_context)

    def form_invalid(self, form):
        response_context = dict(success=False, messages=form.errors)
        return JsonResponse(response_context)


class DataMapImportSettingsView(FormView):
    template_name = ""
    form_class = DataMapImportSettingsForm

    def setup(self):
        datamap_id = self.kwargs.get("datamap_id")
        self.datamap = DataMap.objects.filter(id=datamap_id)

    def get(self, request, *args, **kwargs):
        self.setup()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.setup()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["instance"] = self.datamap
        return form_kwargs

    def form_valid(self, form):
        datamap = form.save()
        task_ids = start_datamap_import_task(datamap)
        response_context = dict(success=True, datamap_id=datamap.id, task_ids=task_ids)
        return JsonResponse(response_context)

    def form_invalid(self, form):
        response_context = dict(success=False, messages=form.errors)
        return JsonResponse(response_context)


class DataMapListJson(View):

    def get(self, request, *args, **kwargs):
        filter_ids = request.GET.get("ids", None)
        if filter_ids:
            filter_id_list = filter_ids.split(",")
            kmlmaps = DataMap.objects.filter(id__in=filter_id_list)
        else:
            kmlmaps = DataMap.objects.all(); 
        context = dict(
            kmlfiles=[dict(id=km.id, title=km.name, source=km.get_file_url()) for km in kmlmaps]
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


class SocrataDatamapMetadata(View):

    def get(self, request, *args, **kwargs):
        datamap_id = kwargs.get("datamap_id")
        datamap = DataMap.objects.get(id=datamap_id)
        metadata = datamap.get_socrata_client().get_metadata(datamap.dataset_identifier)
        return JsonReponse(metadata)


