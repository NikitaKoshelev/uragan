from django.utils.translation import gettext as _
from django import forms
from apps.common.widgets import ColorPickerWidget
from .models import GeoObject


class GeoObjectForm(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = 'title', 'lat', 'lon', 'description', 'short_description', 'polygon'
        widgets = {
            'color': ColorPickerWidget(),
            'short_description': forms.widgets.Textarea(attrs={'rows': 5}),
            'polygon': forms.widgets.Textarea(attrs={'rows': 1}),
        }

    class Media:
         css = {
             'all': ('plugins/select2/css/select2.min.css',)
         }
         js = (
             "plugins/select2/js/select2.full.min.js",
             'uragan/GeoObject_create.min.js'
             #'uragan/create_GeoObject.js',
             #'uragan/nominatim_in_select2.js',
             #'uragan/google_in_select2.js',
         )


class GeoObjectPart2Form(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = 'description', 'short_description', 'polygon'
