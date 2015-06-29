import json

from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, DetailView, ListView, UpdateView
from django.core.serializers import serialize

from formtools.wizard.views import CookieWizardView

from .api import get_kml_for_queryset, get_lst_for_queryset, get_kml_by_object
from .models import GeoObject, SurveillancePlan
from .forms import GeoObjectForm, GeoObjectFormStep1, GeoObjectFormStep2, SurveillancePlanForm
from apps.common.mixins import LoginRequiredMixin
from apps.TLE.mixins import SatellitesTemplateResponseMixin


def where_iss(request):
    return render_to_response('includes/where_is_iss.html')

class CreateGeoObject(CreateView):
    model = GeoObject
    form_class = GeoObjectForm
    template_name = 'GeoObject/GeoObject/create.html'

class DetailGeoObject(SatellitesTemplateResponseMixin, DetailView):
    model = GeoObject
    context_object_name = 'geo_object'
    template_name = 'GeoObject/GeoObject/detail.html'

    def get_kml(self):
        return get_kml_by_object(self.object)

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('get_kml', False):
            return self.get_kml()
        else:
            return super(DetailGeoObject, self).render_to_response(context, **response_kwargs)


class UpdateGeoObject(UpdateView):
    model = GeoObject
    form_class = GeoObjectForm
    # fields = 'lat', 'lon', 'short_description', 'color'
    template_name = 'GeoObject/GeoObject/update.html'

    def get_kml(self):
        return get_kml_by_object(self.object)

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('get_kml', False):
            return self.get_kml()
        else:
            return super(UpdateGeoObject, self).render_to_response(context, **response_kwargs)


class ListGeoObject(SatellitesTemplateResponseMixin, ListView):
    model = GeoObject
    context_object_name = 'geo_objects'
    # paginate_by = 100
    template_name = 'GeoObject/GeoObject/list.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('get_kml', False):
            return get_kml_for_queryset(context['object_list'])
        elif self.request.GET.get('get_lst', False):
            return get_lst_for_queryset(context['object_list'])
        else:
            return super(ListGeoObject, self).render_to_response(context, **response_kwargs)


class WizardCreateGeoObject(CookieWizardView):
    template_name = 'GeoObject/GeoObject/wizard_create.html'
    form_list = (GeoObjectFormStep1, GeoObjectFormStep2)

    def done(self, form_list, **kwargs):
        data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        pk = GeoObject.objects.create(**data).pk
        return redirect('GeoObject:detail', pk=pk)


class CreateSurveillancePlan(LoginRequiredMixin, CreateView):
    model = SurveillancePlan
    form_class = SurveillancePlanForm
    template_name = 'GeoObject/SurveillancePlan/create.html'

    def get_initial(self):
        init = super(CreateSurveillancePlan, self).get_initial()
        init.update({'researchers': [self.request.user.id]})
        return init

    def form_valid(self, form):
        self.object = form.save()
        if self.object.researchers.filter(pk=self.request.user.pk).count():
            self.object.researchers.add(self.request.user)
        return super(CreateSurveillancePlan, self).form_valid(form)


class UpdateSurveillancePlan(LoginRequiredMixin, UpdateView):
    model = SurveillancePlan
    form_class = SurveillancePlanForm
    template_name = 'GeoObject/SurveillancePlan/create.html'


class DetailSurveillancePlan(SatellitesTemplateResponseMixin, DetailView):
    model = SurveillancePlan
    context_object_name = 'surv_plan'
    template_name = 'GeoObject/SurveillancePlan/detail.html'

    def get_kml(self):
        filename = '{} ({}--{})'.format(self.object.title, self.object.time_start.date(), self.object.time_end.date())
        query = self.object.geo_objects.all()
        return get_kml_for_queryset(query, filename)

    def get_lst(self):
        filename = '{} ({}--{})'.format(self.object.title, self.object.time_start.date(), self.object.time_end.date())
        query = self.object.geo_objects.all()
        return get_lst_for_queryset(query, filename)

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('get_kml', False):
            return self.get_kml()
        elif self.request.GET.get('get_lst', False):
            return self.get_lst()
        return super(DetailSurveillancePlan, self).render_to_response(context, **response_kwargs)


class ListSurveillancePlan(SatellitesTemplateResponseMixin, ListView):
    model = SurveillancePlan
    context_object_name = 'surv_plans'
    paginate_by = 20
    template_name = 'GeoObject/SurveillancePlan/list.html'
