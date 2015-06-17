from django.utils.translation import gettext as _
from django.forms import Textarea, HiddenInput
from apps.common.widgets import ColorPickerWidget
from apps.common.forms import BaseModelForm
from .models import GeoObject
from django_select2.widgets import Select2MultipleWidget


class GeoObjectForm(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
            'images': Select2MultipleWidget()
        }

    class Media:
         js = (
             #'uragan/create_GeoObject_step1.min.js'
             'uragan/create_GeoObject_step1.js',
             'uragan/nominatim_in_select2.js',
             'uragan/google_in_select2.js',
         )


class GeoObjectFormStep1(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = 'title', 'lon', 'lat', 'polygon'
        widgets = {
            'polygon': HiddenInput(),
        }

    class Media:
         js = (
             'uragan/forms/create_GeoObject_step1.min.js',
             #'uragan/forms/create_GeoObject_step1.js',
             #'uragan/forms/nominatim_in_select2.js',
             #'uragan/forms/google_in_select2.js',
         )

class GeoObjectFormStep2(BaseModelForm):
    class Meta:
        model = GeoObject
        exclude = 'title', 'lon', 'lat', 'images'
        widgets = {
            'color': ColorPickerWidget(),
            #'images': Select2MultipleWidget(attrs={'style': 'width: 100%'})
        }

    class Media:
        js = (
            'uragan/forms/create_GeoObject_step2.js',
        )