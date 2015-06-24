# coding: utf-8
from geopy import Nominatim, GoogleV3, GeoNames
from yandex_translate import YandexTranslate
from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.http import urlquote
from django.core.serializers import serialize
from django.utils.translation import ugettext_lazy as _

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

            response = JsonResponse(GeoObject.objects.filter(title__icontains=q))
        else:
            response = 'Not valid parameters'
    else:
        response = 'Not get request'

    return HttpResponse(response)


def get_kml_by_object(request, pk):
    obj = get_object_or_404(GeoObject, pk=pk)
    polygon = obj.get_polygon_in_kml()
    response = get_kml_file_response(polygon, obj.title)
    return response


def get_kml_by_title(request):
    if request.GET:
        query = request.GET['title']
        polygon = nominatim.geocode(query=query, geometry='kml').raw['geokml']
        if polygon:
            kml = KML.kml(KML.Document(KML.Placemark(KML.name(query), parser.fromstring(polygon))))
            polygon = etree.tostring(kml)
            response = get_kml_file_response(polygon, query)
        else:
            response = HttpResponseBadRequest()
    else:
        response = HttpResponseBadRequest()

    return response


def get_kml_file_response(kml, filename):
    response = HttpResponse(kml, content_type='application/vnd.google-earth.kml+xml')
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}.kml'.format(urlquote(filename))
    return response


def get_kml_for_queryset(queryset):
    kml = KML.kml(KML.Document())
    for item in queryset.values('title', 'lat', 'lon', 'polygon'):
        polygon = item.get('polygon', None)
        fld = KML.Folder(
            KML.name(item['title']),
            KML.Placemark(KML.name(item['title']), KML.Point(KML.coordinates("{},{}".format(item['lon'], item['lat']))))
        )
        if polygon:
            fld.append(KML.Placemark(KML.name(item['title']), parser.fromstring(polygon)))

        kml.Document.append(fld)
    return get_kml_file_response(etree.tostring(kml), _('Geographical objects'))
