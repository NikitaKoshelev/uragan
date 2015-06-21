# coding: utf-8
import json
from geopy import Nominatim, GoogleV3, GeoNames
from yandex_translate import YandexTranslate

from django.conf import settings
from django.http import HttpResponse
from django.core.serializers import serialize

from .models import GeoObject
from .forms import GeocoderForm

google = GoogleV3('AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw')
nominatim = Nominatim()
geo_names = GeoNames(username='nikita.koshelev@gmail.com')


def geocoder(request, lng=None):
    if request.GET:
        form = GeocoderForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['query']
            if lng:
                translator = YandexTranslate(settings.YANDEX_TRANSLATE_KEY)
                result = translator.translate(q, lng)
                q = result['text'][0] if result['code'] == 200 else q

            local = serialize('json', GeoObject.objects.filter(title__icontains=q), fields=('title', 'lat', 'lon'))
            data = {'results': [{'text': 'Locals', 'children':  local}, ]}
            #data['results'].append({'text': 'Nominatim', 'children': nominatim.geocode(q, exactly_one=False)})
            #data['results'].append({'text': 'Geo Names', 'children': geo_names.geocode(q, exactly_one=False)})
            data['results'].append({'text': 'Google', 'children': google.geocode(q, exactly_one=False)})
            response = json.dumps(data) if data['results'] else 'Not found'
            print(data)
        else:
            response = 'Not valid parameters'
    else:
        response = 'Not get request'

    return HttpResponse(response)
