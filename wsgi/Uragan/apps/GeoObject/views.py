from django.shortcuts import render_to_response
from django.views.generic import CreateView, DeleteView, FormView
from .forms import GeoObjectForm#,GeoObjectPart1Form
from apps.common.mixins import LoginRequiredMixin


def where_iss(request):
    return render_to_response('includes/where_is_iss.html')


class CreateGeoObject(CreateView):
    form_class = GeoObjectForm

    template_name = 'GeoObject/GeoObject_form.html'



