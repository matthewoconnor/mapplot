from django import forms

from .models import KmlMap

class KmlmapForm(forms.ModelForm):

	class Meta:
		model = KmlMap
		exclude = []