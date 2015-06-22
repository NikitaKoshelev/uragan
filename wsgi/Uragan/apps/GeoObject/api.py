# coding: utf-8
import json
from geopy import Nominatim, GoogleV3, GeoNames
from yandex_translate import YandexTranslate

from django.conf import settings
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404
from django.http import HttpResponse
from django.core.serializers import serialize

from .models import GeoObject
from .forms import GeocoderForm

google = GoogleV3('AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw')
nominatim = Nominatim()
geo_names = GeoNames(username='nikita.koshelev@gmail.com')


def geocoder(request, lang=None):
    if request.GET:
        form = GeocoderForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['query']
            if lang:
                translator = YandexTranslate(settings.YANDEX_TRANSLATE_KEY)
                result = translator.translate(q, lang)
                q = result['text'][0] if result['code'] == 200 else q

            response = serialize('json', GeoObject.objects.filter(title__icontains=q))
        else:
            response = 'Not valid parameters'
    else:
        response = 'Not get request'

    return HttpResponse(response)


def get_kml(request, pk):
    obj = get_object_or_404(GeoObject, pk=pk)
    polygon = obj.get_polygon_in_kml()
    response = HttpResponse(polygon)
    response['Content-Disposition'] = 'attachment; filename="{}.kml"'.format(obj.get_translate_title())
    return response