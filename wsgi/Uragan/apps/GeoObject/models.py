# coding: utf-8
#from django.contrib.gis.db import models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone as tz

from datetime import timedelta
from django.conf import settings

class Images(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    image = models.ImageField(upload_to='geo_objects', verbose_name=_('image'))

    class Meta:
        verbose_name = _('geographical object image')
        verbose_name_plural = _('images of geographical objects')


class GeoObject(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title geographical object'), unique=True)
    lat = models.FloatField(verbose_name=_('northern latitude in degrees'))
    lon = models.FloatField(verbose_name=_('eastern longitude in degrees'))
    short_description = models.TextField(verbose_name=_('short description'), null=True, blank=True)
    description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    polygon = models.TextField(verbose_name=_('polygon in KML format'), null=True, blank=True)
    color = models.TextField(verbose_name=_('color'), null=True, blank=True)
    images = models.ManyToManyField(Images, verbose_name=_('images of geographical object'), blank=True)

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