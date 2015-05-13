from django.utils.translation import gettext as _
from django.forms import ModelForm, widgets
from apps.common.widgets import ColorPickerWidget
from .models import GeoObject


class GeoObjectForm(ModelForm):

    class Meta:
        model = GeoObject
        fields = '__all__'
        widgets = {
            'color': ColorPickerWidget(),
            'short_description': widgets.Textarea(attrs={'rows': 5})
        }