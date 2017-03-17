from django import forms

from .models import DataMap


class KmlmapForm(forms.ModelForm):
    where = forms.CharField(required=False)
    limit = forms.IntegerField(required=False, initial=1000)
    categorize_method = forms.ChoiceField(required=False, choices=[
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
        model = DataMap
        fields = ["name", "data_source", "dataset_identifier", "area_map"]


class DataMapCreateForm(forms.ModelForm):

    class Meta:
        model = DataMap
        fields = ["name", "data_source", "dataset_identifier", "area_map"]


class DataMapImportSettingsForm(forms.ModelForm):

    class Meta:
        model = DataMap
        fields = ["categorize_type", "latitude_key", "longitude_key",
                  "point_key", "join_key", "weight_type", "value_key",
                  "querystring"]




