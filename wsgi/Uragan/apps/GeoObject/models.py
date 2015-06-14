# coding: utf-8
#from django.contrib.gis.db import models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone as tz

from datetime import timedelta
from django.conf import settings

class Images(models.Model):
    geo_object = models.ForeignKey('GeoObject', verbose_name=_('geographical object'))
    image = models.ImageField(upload_to='geo_objects', verbose_name=_('image'))

    class Meta:
        verbose_name = _('geographical object image')
        verbose_name_plural = _('images of geographical objects')


class GeoObject(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title geographical object'), unique=True)
    #location = models.PointField(verbose_name=_('location'), unique=True)
    lat = models.FloatField(verbose_name=_('north latitude in degrees'))
    lon = models.FloatField(verbose_name=_('east longitude in degrees'))
    short_description = models.TextField(verbose_name=_('short description'))
    description = models.TextField(verbose_name=_('description'))
    polygon = models.TextField(verbose_name=_('polygon in KML format'), null=True)
    color = models.TextField(verbose_name=_('color'), null=True)

    class Meta:
        unique_together = 'lat', 'lon',
        verbose_name = _('geographical object')
        verbose_name_plural = _('geographical objects')


class SurveillancePlan(models.Model):
    geo_objects = models.ManyToManyField(GeoObject, verbose_name=_('observed objects'))
    time_start = models.DateTimeField(auto_now=True)
    time_end = models.DateTimeField(default=tz.now()+timedelta(days=3))
    researches = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('researches'))

    class Meta:
        verbose_name = _('surveillance plan')
        verbose_name_plural = _('surveillance plans')