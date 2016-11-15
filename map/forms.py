from django import forms

from .models import KmlMap

class KmlmapForm(forms.ModelForm):

	search_kwargs = forms.CharField()
	limit = forms.IntegerField(required=True, initial=1000)
	name = forms.CharField()
	data_source = forms.CharField()
	dataset_identifier = forms.CharField()
	area_map = forms.Select()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields["name"].widget.attrs.update({"ng-model":"kmlmap.name"})
		self.fields["data_source"].widget.attrs.update({"ng-model":"kmlmap.data_source"})
		self.fields["dataset_identifier"].widget.attrs.update({"ng-model":"kmlmap.dataset_identifier"})
		self.fields["area_map"].widget.attrs.update({"ng-model":"kmlmap.area_map"})
		self.fields["search_kwargs"].widget.attrs.update({"ng-model":"kmlmap.search_kwargs"})
		self.fields["limit"].widget.attrs.update({"ng-model":"kmlmap.limit"})


	class Meta:
		model = KmlMap
		fields = ["name", "data_source", "dataset_identifier", "area_map"]