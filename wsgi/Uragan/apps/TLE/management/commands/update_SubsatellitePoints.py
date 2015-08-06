# coding: utf-8
from django.core.management.base import BaseCommand
from django.core.cache import caches
from datetime import timedelta
from apps.TLE.utils import update_track
from apps.TLE.models import SubsatellitePoint, TLE


class Command(BaseCommand):
    help = 'Update SubsatellitePoints'

    def handle(self, **options):
        tle = TLE.objects.filter(satellite=25544).first()
        if tle.subsatellitepoint_set.count() == 0:
            try:
                self.stdout.write('Start create and save SubsatellitePoints\n')
                caches['subsatpoints'].clear()
                for k, v in update_track(tle, delta=timedelta(days=1)):
                    print(k)
                    caches['subsatpoints'].add(k, v)
                caches['subsatpoints'].add('countries', ['ru', 'us'])
                self.stdout.write('\nFinished create and save SubsatellitePoints\n')
            except:
                self.stdout.write('Fail create and save SubsatellitePoints\n')
        else:
            self.stdout.write('Create new SubsatellitePoints aborted. No new TLE.\n')