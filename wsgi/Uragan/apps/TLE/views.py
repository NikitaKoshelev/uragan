import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.generic import ListView, DayArchiveView, TodayArchiveView
from apps.TLE.models import TLE


class TLE_ListView(ListView):
    model = TLE
    paginate_by = 10
    template_name = 'TLE/list.html'

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


class TLETodayArchiveView(TodayArchiveView):
    model = TLE
    date_field = "datetime_in_lines"
    template_name = 'TLE/TLE/archive/day.html'

