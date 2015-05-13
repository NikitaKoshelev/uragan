from django.shortcuts import render
from django.views.generic import CreateView
from .forms import GeoObjectForm
from apps.common.mixins import LoginRequiredMixin


class CreateGeoObject(LoginRequiredMixin, CreateView):
    form_class = GeoObjectForm
    template_name = 'GeoObject/GeoObject_form.html'



