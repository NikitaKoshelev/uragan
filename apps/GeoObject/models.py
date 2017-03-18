# coding: utf-8
from datetime import timedelta

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point
from django.core.urlresolvers import reverse
from django.utils import timezone as tz
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import Nominatim
from lxml import etree
from pykml import parser
from pykml.factory import KML_ElementMaker as KML
from yandex_translate import YandexTranslate

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
    color = models.CharField(max_length=20, verbose_name=_('color'), default='#0000ff', null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    geometry = models.GeometryField(srid=4326, verbose_name=_('geometry in KML format'), null=True, blank=True)
    images = models.ManyToManyField(Images, verbose_name=_('images of geographical object'), blank=True)
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_('last modification'))
    lat = models.FloatField(verbose_name=_('northern latitude in degrees'))
    location = models.PointField(geography=True, spatial_index=True, srid=4326, verbose_name=_('location point'),
                                 null=True, unique=True)
    lon = models.FloatField(verbose_name=_('eastern longitude in degrees'))
    short_description = models.TextField(verbose_name=_('short description'), null=True, blank=True)
    title = models.TextField(verbose_name=_('title geographical object'), unique=True, db_index=True)

    objects = models.GeoManager

    class Meta:
        ordering = 'title',
        verbose_name = _('geographical object')
        verbose_name_plural = _('geographical objects')

    def __iter__(self):
        # data = serialize('json', self)
        # print(data)
        for field in self._meta.fields:
            yield (field.name, capfirst(field.verbose_name), capfirst(field.value_to_string(self)))

    def get_translate_title(self, lang='en'):
        translator = YandexTranslate(settings.YANDEX_TRANSLATE_KEY)
        result = translator.translate(self.title, lang)
        return result['text'][0] if result['code'] == 200 else self.title

    def get_geometry_in_kml(self, full=True, placemark=False):
        geometry = self.geometry
        if geometry:
            if full:
                line_color, geometry_color = convert_color_hex_to_kml(self.color)
                id = 'geo_object_%s' % self.id
                kml = KML.kml(KML.Document(
                    KML.Style(
                        KML.PolyStyle(KML.color(geometry_color)),
                        KML.LineStyle(KML.color(line_color), KML.width(2)),
                        id=id
                    ),
                    KML.Placemark(KML.name(self.title), KML.styleUrl('#' + id), parser.fromstring(self.geometry.kml))
                ))
                geometry = etree.tostring(kml, pretty_print=True)

            elif placemark:
                kml = KML.Placemark(KML.name(self.title), parser.fromstring(self.geometry.kml))
                geometry = etree.tostring(kml, pretty_print=True)

            else:
                geometry = self.geometry.kml

        return geometry

    def get_WKT_from_nominatim(self):
        try:
            return Nominatim().geocode(self.title, geometry='wkt').raw.get('geotext', None)
        except:
            return None

    def get_absolute_url(self):
        return reverse('GeoObject:detail', args=[self.pk])

    def save(self, *args, **kwargs):
        wkt = self.get_WKT_from_nominatim()
        if wkt:
            self.geometry = GEOSGeometry(wkt)
        self.location = Point(self.lon, self.lat, srid=4326)
        return super(GeoObject, self).save(*args, **kwargs)

    def __str__(self):
        return '{}{}'.format(self.title, self.location)


class SurveillancePlan(models.Model):
    title = models.TextField(verbose_name=_('title surveillance plan'))
    short_description = models.TextField(verbose_name=_('short description'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    geo_objects = models.ManyToManyField(GeoObject, verbose_name=_('observed objects'))
    time_start = models.DateTimeField(auto_now=True, verbose_name=_('date and time start'))
    time_end = models.DateTimeField(default=tz.now() + timedelta(days=7), verbose_name=_('date and time end'))
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date and time'))
    last_modification = models.DateTimeField(auto_now=True, verbose_name=_('modification date and time'))
    researchers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('researchers'), blank=True)

    class Meta:
        verbose_name = _('surveillance plan')
        verbose_name_plural = _('surveillance plans')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('GeoObject:detail_plan', self.pk)
