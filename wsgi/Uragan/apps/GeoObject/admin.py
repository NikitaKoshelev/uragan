from reversion import VersionAdmin
from suit.widgets import AutosizedTextarea
from django_select2.widgets import Select2MultipleWidget

from django.contrib import admin
from django.forms import ModelForm

from .models import GeoObject, Images, SurveillancePlan
from apps.common.widgets import ColorPickerWidget

class GeoObjectAdminForm(ModelForm):
    class Meta:
        widgets = {
            'title': AutosizedTextarea,
            'short_description': AutosizedTextarea,
            'description': AutosizedTextarea,
            'color': ColorPickerWidget,
            'images': Select2MultipleWidget,
        }


class GeoObjectAdmin(VersionAdmin):
    form = GeoObjectAdminForm
    list_display = ('title', 'lat', 'lon', 'short_description',)

class ImagesAdmin(VersionAdmin):
    list_display = ('title', 'image',)

class SurveillancePlanAdmin(VersionAdmin):
    pass


admin.site.register(GeoObject, GeoObjectAdmin)
admin.site.register(SurveillancePlan, SurveillancePlanAdmin)
admin.site.register(Images, ImagesAdmin)