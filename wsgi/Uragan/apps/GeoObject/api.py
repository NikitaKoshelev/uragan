# coding: utf-8
import tempfile
from geopy import Nominatim, GoogleV3, GeoNames
from yandex_translate import YandexTranslate
from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, FileResponse
from django.utils.http import urlquote
from django.core.serializers import serialize
from django.utils.translation import ugettext_lazy as _

from .models import GeoObject
from .forms import GeocoderForm, KmlByTitle
from .utils import convert_color_hex_to_kml


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
    response = get_file_response(polygon, obj.title)
    return response


def get_kml_by_title(request):
    if request.GET:
        query = request.GET['title']
        polygon = nominatim.geocode(query=query, geometry='kml').raw['geokml']
        if polygon:
            kml = KML.kml(KML.Document(KML.Placemark(KML.name(query), parser.fromstring(polygon))))
            polygon = etree.tostring(kml)
            response = get_file_response(polygon, query)
        else:
            response = HttpResponseBadRequest()
    else:
        response = HttpResponseBadRequest()

    return response


def get_file_response(kml, filename, content_type='application/vnd.google-earth.kml+xml', fmt='kml'):
    response = HttpResponse(kml, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}.{}'.format(urlquote(filename), fmt)
    return response


def get_kml_for_queryset(queryset):
    """
    :param queryset: GeoObject queryset
    :return: KML file from GeoObject queryset
    """
    kml = KML.kml(KML.Document())
    for item in queryset.values('title', 'lat', 'lon', 'polygon', 'color', 'id'):
        polygon = item.get('polygon', None)
        line_color, polygon_color = convert_color_hex_to_kml(item['color'])
        fld = KML.Folder(
            KML.name(item['title']),
            KML.Placemark(KML.name(item['title']), KML.Point(KML.coordinates("{},{}".format(item['lon'], item['lat']))))
        )
        if polygon:
            print(line_color, polygon_color)
            id = 'geo_object_%s' % item['id']
            fld.append(KML.Style(
                KML.PolyStyle(KML.color(polygon_color)),
                KML.LineStyle(KML.color(line_color), KML.width(2)),
                id=id))
            fld.append(KML.Placemark(KML.name(item['title']), KML.styleUrl('#' + id), parser.fromstring(polygon)))

        kml.Document.append(fld)

    return get_file_response(etree.tostring(kml), _('Geographical objects'))


def get_lst_for_queryset(queryset):
    lines = [
        "{} {} '{}'".format(item['lon'], item['lat'], item['title']) for item in queryset.values('title', 'lat', 'lon')
        ]
    handle, tmp_path = tempfile.mkstemp()
    tmp = open(tmp_path, 'w', encoding='cp866')
    tmp.write('\r\n'.join(lines))
    response = FileResponse(open(tmp_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}.lst'.format(urlquote(_('Geographical objects')))
    return response
