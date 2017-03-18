__author__ = 'koshelev'
import json

from django.http import HttpResponse
from django.core.serializers import serialize

from apps.TLE.models import Satellite
from apps.TLE.forms import TleApiForm


def satellites_list(request, **kwargs):
    fmt = kwargs.get('fmt', 'json')
    if fmt in ('json', 'xml'):
        data = serialize(fmt.lower(), Satellite.objects.all(), fields=('title','satellite_number'))
        return HttpResponse(data)
    else:
        return HttpResponse('Неизвестный формат')

def tle(request, fmt='json'):
    form = TleApiForm(request.GET)
    print(form, form.is_valid())
    if form.is_valid():
        satellite = Satellite.objects.get(form['satellite_id'].clear())
        if satellite:
            tle = satellite.tle_set.filter(datetime_in_lines__gte=form['datetime_start']).filter(datetime_in_lines__lte=form['datetime_end'])
            data = serialize('json', tle, fields=('datetime_in_lines', 'title_line', 'line1', 'line2'))
            return HttpResponse(json.dumps([obj['fields'] for obj in json.loads(data)]))
    else:
        return HttpResponse(form)