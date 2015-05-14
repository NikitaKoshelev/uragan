from django.utils.translation import gettext as _
from django import forms
from apps.common.widgets import ColorPickerWidget
from .models import GeoObject


class GeoObjectForm(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
            'short_description': forms.widgets.Textarea(attrs={'rows': 5}),
        }


class GeoObjectPart1Form(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = 'title', 'lat', 'lon'
        widgets = {
            'title': forms.widgets.TextInput(attrs={'style': 'display: none;'})
        }

    class Media:
         css = {
             'all': ('plugins/select2/css/select2.min.css',)
         }
         js = (
             'uragan/geoxml3.js',
             "plugins/select2/js/select2.full.min.js",
             'uragan/GeoObject_create_part1.js',
         )


class GeoObjectPart2Form(forms.ModelForm):
    class Meta:
        model = GeoObject
        fields = 'description', 'short_description', 'polygon'
