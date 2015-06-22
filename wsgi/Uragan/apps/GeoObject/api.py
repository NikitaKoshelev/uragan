# coding: utf-8
import json
from geopy import Nominatim, GoogleV3, GeoNames
from yandex_translate import YandexTranslate
from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree

from django.conf import settings
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.serializers import serialize

from .models import GeoObject
from .forms import GeocoderForm, KmlByTitle

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


def get_kml_by_object(request, pk):
    obj = get_object_or_404(GeoObject, pk=pk)
    polygon = obj.get_polygon_in_kml()
    response = HttpResponse(polygon)
    response['Content-Disposition'] = 'attachment; filename="{}.kml"'.format(obj.get_translate_title())
    return response

def get_kml_by_title(request):
    if request.GET:
        query = request.GET['title']
        polygon = nominatim.geocode(query=query, geometry='kml').raw['geokml']
        if polygon:
            kml = KML.kml(KML.Document(KML.Placemark(KML.name(query), parser.fromstring(polygon))))
            polygon = etree.tostring(kml, pretty_print=True)
            response = HttpResponse(polygon)
            translator = YandexTranslate(settings.YANDEX_TRANSLATE_KEY)
            result = translator.translate(query, 'en')
            q = result['text'][0] if result['code'] == 200 else query
            response['Content-Disposition'] = 'attachment; filename="{}.kml"'.format(q)
        else:
            response = HttpResponseBadRequest()
    else:
        response = HttpResponseBadRequest()

    return response

