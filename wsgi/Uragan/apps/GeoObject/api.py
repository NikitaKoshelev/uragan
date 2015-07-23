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
from .forms import GeocoderForm
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


def get_kml_by_object_id(request, pk):
    obj = get_object_or_404(GeoObject, pk=pk)
    polygon = obj.get_geometry_in_kml()
    response = get_file_response(polygon, obj.title)
    return response


def get_kml_by_object(obj):
    polygon = obj.get_geometry_in_kml()
    response = get_file_response(polygon, obj.title)
    return response


def get_kml_by_title(request):
    if request.GET or request.is_ajax():
        query = request.GET['title']
        result = nominatim.geocode(query=query, geometry='kml')
        polygon = result.raw['geokml'] if result else None
        if polygon:
            polygon = result.raw['geokml']
            kml = KML.kml(KML.Document(KML.Placemark(KML.name(query), parser.fromstring(polygon))))
            polygon = etree.tostring(kml)
            response = get_file_response(polygon, query)
        else:
            response = HttpResponseBadRequest('Not found')
    else:
        response = HttpResponseBadRequest('Request is not GET')

    return response


def get_file_response(kml, filename, content_type='application/vnd.google-earth.kml+xml', fmt='kml'):
    response = HttpResponse(kml, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}.{}'.format(urlquote(filename), fmt)
    return response


def get_kml_for_queryset(queryset, filename=_('Geographical objects')):
    """
    :param queryset: GeoObject queryset
    :return: KML file from GeoObject queryset
    """
    kml = KML.kml(KML.Document(KML.open(1)))

    geo_objects = queryset.values_list('color', 'title', 'lat', 'lon', 'polygon', 'short_description')
    colors = set(items[0] for items in sorted(geo_objects))
    colors_dict = {color: convert_color_hex_to_kml(color) for color in colors}

    for line_color, polygon_color in colors_dict.values():
        kml.Document.append(KML.Style(
            KML.PolyStyle(KML.color(polygon_color)),
            KML.LineStyle(KML.color(line_color), KML.width(2)),
            id=line_color,
        ))
        print(line_color, polygon_color)

    for (color, title, lat, lon, polygon, short_description) in geo_objects:
            style_id = colors_dict[color][0]
            fld = KML.Folder(
                KML.name(title),
                KML.Placemark(
                    KML.name(title),
                    KML.styleUrl('#' + style_id),
                    KML.description(short_description),
                    KML.Point(KML.coordinates("{},{},0".format(lon, lat)))
                )
            )

            if polygon:
                polygon = parser.fromstring(polygon)
                fld.append(KML.Placemark(KML.name(title), KML.styleUrl('#' + style_id),
                                         KML.description(short_description), polygon))

            kml.Document.append(fld)

    kml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(kml, pretty_print=True).decode()
    return get_file_response(kml_str, filename)


def get_lst_for_queryset(queryset, filename=_('Geographical objects')):
    lines = [
        "{} {} '{}'".format(item['lon'], item['lat'], item['title']) for item in queryset.values('title', 'lat', 'lon')
        ]
    handle, tmp_path = tempfile.mkstemp()
    tmp = open(tmp_path, 'w', encoding='cp866')
    tmp.write('\r\n'.join(lines))
    response = FileResponse(open(tmp_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}.lst'.format(urlquote(filename))
    return response
