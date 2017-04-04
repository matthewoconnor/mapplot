from django import forms

from .models import DataMap


class DataMapForm(forms.ModelForm):

    class Meta:
        model = DataMap
        fields = ["name", "data_source", "dataset_identifier", "area_map"]


class DataMapImportSettingsForm(forms.ModelForm):

    class Meta:
        model = DataMap
        fields = ["categorize_type", "latitude_key", "longitude_key",
                  "point_key", "join_key", "weight_type", "value_key",
                  "querystring"]




