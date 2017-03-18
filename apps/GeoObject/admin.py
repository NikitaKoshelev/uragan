from django.contrib import admin
from django.forms import ModelForm
from django_select2.widgets import Select2MultipleWidget
from reversion import VersionAdmin
from suit.widgets import AutosizedTextarea

from apps.common.widgets import ColorPickerWidget
from .models import GeoObject, Images, SurveillancePlan


class GeoObjectAdminForm(ModelForm):
    class Meta:
        widgets = {
            'title': AutosizedTextarea,
            'short_description': AutosizedTextarea,
            'description': AutosizedTextarea,
            'color': ColorPickerWidget,
            'images': Select2MultipleWidget(attrs={'style': 'width: 100%'}),
        }


class SurveillancePlanAdminForm(ModelForm):
    class Meta:
        widgets = {
            'title': AutosizedTextarea,
            'geo_objects': Select2MultipleWidget(attrs={'style': 'width: 100%'}),
            'researches': Select2MultipleWidget(attrs={'style': 'width: 100%'}),
        }


class GeoObjectAdmin(VersionAdmin):
    form = GeoObjectAdminForm
    list_display = ('title', 'lat', 'lon', 'short_description',)


class ImagesAdmin(VersionAdmin):
    list_display = ('title', 'image',)


class SurveillancePlanAdmin(VersionAdmin):
    form = SurveillancePlanAdminForm


admin.site.register(GeoObject, GeoObjectAdmin)
admin.site.register(SurveillancePlan, SurveillancePlanAdmin)
admin.site.register(Images, ImagesAdmin)
