from django.utils.translation import gettext as _
from django.forms import Textarea, HiddenInput, Form, CharField, TextInput
from apps.common.widgets import (ColorPickerWidget, StaticWidget, WYSIHTML5Widget, AutosizedTextarea,
                                 Select2Widget, MultipleSelect2Widget, DateTimePickerWidget)
from apps.common.forms import BaseModelForm
from .models import GeoObject, SurveillancePlan



class GeoObjectFormStep1(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = 'title', 'lon', 'lat'
        widgets = {
            'title': AutosizedTextarea,
            #'images': Select2MultipleWidget(attrs={'style': 'width: 100%'})
        }

    class Media:
         js = (
             #'uragan/forms/create_GeoObject_step1.min.js',
             'uragan/forms/create_GeoObject_step1.js',
             #'uragan/forms/nominatim_in_select2.js',
             'uragan/forms/geocoders.js',
         )


class GeoObjectFormStep2(BaseModelForm):
    class Meta:
        model = GeoObject
        fields = 'short_description', 'description', 'color'
        widgets = {
            'short_description': WYSIHTML5Widget,
            'description': WYSIHTML5Widget,
            'color': ColorPickerWidget,
            'images': MultipleSelect2Widget,
        }



class GeoObjectForm(GeoObjectFormStep1, GeoObjectFormStep2, BaseModelForm):
    class Meta:
        model = GeoObject
        fields = '__all__'
        exclude = 'polygon',
        widgets = GeoObjectFormStep1.Meta.widgets.copy()
        widgets.update(GeoObjectFormStep2.Meta.widgets.copy())


class SurveillancePlanForm(BaseModelForm):
    class Meta:
        model = SurveillancePlan
        fields = '__all__'
        widgets = {
            'title': AutosizedTextarea,
            'short_description': WYSIHTML5Widget,
            'description': WYSIHTML5Widget,
            'geo_objects': MultipleSelect2Widget,
            'researchers': MultipleSelect2Widget,
            'time_end': DateTimePickerWidget,
        }

class GeocoderForm(Form):
    query = CharField(min_length=2)