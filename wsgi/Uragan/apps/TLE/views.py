import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import ListView, DayArchiveView, TodayArchiveView, DetailView
from .models import TLE, Satellite
from .mixins import SatellitesTemplateResponseMixin


class TLE_ListView(SatellitesTemplateResponseMixin, ListView):
    model = TLE
    paginate_by = 50
    template_name = 'TLE/TLE/list.html'


class TLEDayArchiveView(DayArchiveView):
    model = TLE
    month_format = '%m'
    date_field = "datetime_in_lines"
    template_name = 'TLE/TLE/archive/day.html'

    def render_to_json_response(self, context):
        return serialize('json', context['object_list'])

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            print(JsonResponse(context, **response_kwargs))
            return JsonResponse(context, **response_kwargs)
        else:
            return super(TLEDayArchiveView, self).render_to_response(context, **response_kwargs)


class TLETodayArchiveView(SatellitesTemplateResponseMixin, TodayArchiveView):
    model = TLE
    date_field = "datetime_in_lines"
    template_name = 'TLE/TLE/archive/day.html'


class SatelliteDetailView(SatellitesTemplateResponseMixin, DetailView):
    model = Satellite
    template_name = 'TLE/Satellites/detail.html'


class SatelliteListView(SatellitesTemplateResponseMixin, ListView):
    queryset = Satellite.objects.all().order_by('title')
    template_name = 'TLE/Satellites/list.html'
