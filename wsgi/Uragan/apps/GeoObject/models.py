# coding: utf-8
from geopy.geocoders import Nominatim
from pykml.factory import KML_ElementMaker as KML
from pykml import parser
from lxml import etree
from yandex_translate import YandexTranslate

# from django.contrib.gis.db import models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone as tz
from datetime import timedelta
from django.conf import settings
from django.utils.text import capfirst

from .utils import convert_color_hex_to_kml


class Images(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    image = models.ImageField(upload_to='geo_objects/images/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('geographical object image')
        verbose_name_plural = _('images of geographical objects')

    def __str__(self):
        return self.title


class GeoObject(models.Model):
    title = models.TextField(verbose_name=_('title geographical object'), unique=True)
    lat = models.FloatField(verbose_name=_('northern latitude in degrees'))
    lon = models.FloatField(verbose_name=_('eastern longitude in degrees'))
    short_description = models.TextField(verbose_name=_('short description'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    polygon = models.TextField(verbose_name=_('polygon in KML format'), null=True, blank=True)
    color = models.CharField(max_length=20, verbose_name=_('color'), default='#0000ff', null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_('last modification'))
    images = models.ManyToManyField(Images, verbose_name=_('images of geographical object'), blank=True)

    class Meta:
        ordering = 'title',
        unique_together = 'lat', 'lon',
        verbose_name = _('geographical object')
        verbose_name_plural = _('geographical objects')

    def __iter__(self):
        #data = serialize('json', self)
        #print(data)
        for field in self._meta.fields:
            yield (field.name, capfirst(field.verbose_name), capfirst(field.value_to_string(self)))

    def get_translate_title(self, lang='en'):
        translator = YandexTranslate(settings.YANDEX_TRANSLATE_KEY)
        result = translator.translate(self.title, lang)
        return result['text'][0] if result['code'] == 200 else self.title

    def get_polygon_in_kml(self, full=True, placemark=False):
        polygon = self.polygon
        if polygon:
            if full:
                line_color, polygon_color = convert_color_hex_to_kml(self.color)
                id = 'geo_object_%s' % self.id
                kml = KML.kml(KML.Document(
                    KML.Style(
                        KML.PolyStyle(KML.color(polygon_color)),
                        KML.LineStyle(KML.color(line_color), KML.width(2)),
                        id=id
                    ),
                    KML.Placemark(KML.name(self.title),  KML.styleUrl('#' + id), parser.fromstring(self.polygon))
                ))
                polygon = etree.tostring(kml, pretty_print=True)

            elif placemark:
                kml = KML.Placemark(KML.name(self.title), parser.fromstring(self.polygon))
                polygon = etree.tostring(kml, pretty_print=True)

            else:
                polygon = etree.tostring(self.polygon, pretty_print=True)

        return polygon

    def save(self, *args, **kwargs):
        try:
            kml = Nominatim().geocode(self.title, geometry='kml').raw.get('geokml', False)
            if kml:
                self.polygon = kml
        except:
            pass
        return super(GeoObject, self).save(*args, **kwargs)

    def __str__(self):
        return '{}({}, {})'.format(self.title, self.lat, self.lon)


class SurveillancePlan(models.Model):
    title = models.TextField(verbose_name=_('title surveillance plan'))
    geo_objects = models.ManyToManyField(GeoObject, verbose_name=_('observed objects'))
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(default=tz.now() + timedelta(days=3))
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_('date and time created'))
    researchers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('researchers'))

    class Meta:
        verbose_name = _('surveillance plan')
        verbose_name_plural = _('surveillance plans')

    def __str__(self):
        return self.title