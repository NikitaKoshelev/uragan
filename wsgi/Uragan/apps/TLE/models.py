from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class TLE(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_('date and time of creation'))
    title_line = models.CharField(max_length=24, verbose_name=_('title in line two-line element set'))
    line1 = models.CharField(max_length=69, verbose_name=_('first line in two-line element set'))
    line2 = models.CharField(max_length=69, verbose_name=_('second line in two-line element set'))
    datetime_in_lines = models.DateTimeField(verbose_name=_('date and time in two-line element set'), blank=True)

    satellite = models.ForeignKey('Satellite', to_field='satellite_number')

    class Meta:
        unique_together = ('datetime_in_lines', 'satellite')
        get_latest_by = 'datetime_in_lines'
        ordering = ['-datetime_in_lines']
        db_table = 'TLE'
        verbose_name = _('two-line element set')
        verbose_name_plural = _('two-line element sets')

    def __str__(self):
        return '{} ({})'.format(self.title_line, self.datetime_in_lines.isoformat())


class Satellite(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('satellite title'))
    satellite_number = models.IntegerField(verbose_name=_('number of satellites in the database NORAD'),
                                           unique=True)
    about_satellite = models.TextField(verbose_name=_('about satellite'), null=True)
    image = models.ImageField(upload_to='satellites', verbose_name=_('satellite image'), null=True)

    class Meta:
        db_table = 'Satellites'
        verbose_name = _('satellite')
        verbose_name_plural = _('satellites')

    def __str__(self):
        return '{} ({})'.format(self.title, self.satellite_number)


class SubsattellitePoints(models.Model):
    satellite = models.ForeignKey(Satellite)
    datetime = models.DateTimeField(verbose_name=_('date and time'))
    location = models.PointField(verbose_name=_('subsatellite point location'), geography=True)

    class Meta:
        ordering = '-datetime',
        verbose_name = _('subsatellite point')
        verbose_name_plural = _('subsatellite points')

    def __str__(self):
        return '{}: '.format(self._meta.verbose_name)

    objects = models.GeoManager()
