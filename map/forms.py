from django import forms

from .models import KmlMap

class KmlmapForm(forms.ModelForm):

	search_kwargs = forms.CharField()
	limit = forms.IntegerField(required=True, initial=1000)
	categorize_method=forms.ChoiceField(required=True, choices=[
		("LATLNG", "Latitude and Longitude Fields"),
		("POINT", "Point Field"),
		("MATCH", "Matching Field Values")
	])
	lat_field=forms.CharField()
	lng_field=forms.CharField()
	point_field=forms.CharField()
	match_soda_field=forms.CharField()
	match_area_field=forms.CharField()

	class Meta:
		model = KmlMap
		fields = ["name", "data_source", "dataset_identifier", "area_map"]