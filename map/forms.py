from django import forms

from .models import KmlMap

class KmlmapForm(forms.ModelForm):

	where = forms.CharField(required=False)
	limit = forms.IntegerField(required=False, initial=1000)
	categorize_method=forms.ChoiceField(required=False, choices=[
		("LATLNG", "Latitude and Longitude Fields"),
		("POINT", "Point Field"),
		("MATCH", "Matching Field Values")
	])
	lat_field=forms.CharField(required=False)
	lng_field=forms.CharField(required=False)
	point_field=forms.CharField(required=False)
	match_soda_field=forms.CharField(required=False)
	match_area_field=forms.CharField(required=False)

	class Meta:
		model = KmlMap
		fields = ["name", "data_source", "dataset_identifier", "area_map"]