from django.utils.translation import gettext as _
from django import forms
from apps.common.widgets import ColorPickerWidget
from apps.common.forms import BaseModelForm
from .models import GeoObject


class GeoObjectForm(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = '__all__'

        widgets = {
            'color': ColorPickerWidget(),
        }

    class Media:
         js = (
             #'uragan/GeoObject_create.min.js'
             'uragan/create_GeoObject.js',
             'uragan/nominatim_in_select2.js',
             'uragan/google_in_select2.js',
         )

class GeoObjectFormStep1(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = 'title', 'lon', 'lat'

class GeoObjectFormStep2(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = 'description', 'short_description', 'polygon'
