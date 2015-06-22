import json

from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, DetailView

from formtools.wizard.views import CookieWizardView

from .models import GeoObject
from .forms import GeoObjectForm, GeoObjectFormStep1, GeoObjectFormStep2
from apps.common.mixins import LoginRequiredMixin


def where_iss(request):
    return render_to_response('includes/where_is_iss.html')


class DetailGeoObject(DetailView):
    model = GeoObject
    context_object_name = 'geo_object'
    template_name = 'GeoObject/detail.html'


class WizardCreateGeoObject(CookieWizardView):
    template_name = 'GeoObject/wizard_create.html'
    form_list = (GeoObjectFormStep1, GeoObjectFormStep2)

    def done(self, form_list, **kwargs):
        data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        pk = GeoObject.objects.create(**data).pk
        return redirect('GeoObject:detail', pk=pk)
