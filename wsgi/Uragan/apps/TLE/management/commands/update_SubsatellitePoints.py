# coding: utf-8
from django.core.management.base import BaseCommand
from apps.TLE.utils import update_track
from apps.TLE.models import SubsatellitePoint, TLE



class Command(BaseCommand):
    help = 'Update SubsatellirPoints'

    def handle(self, **options):
        tle = TLE.objects.filter(satellite=25544).first()
        if tle.subsatellitepoint_set.count() == 0:
            try:
                self.stdout.write('Start create and save SubsattellitePoints\n')
                tracker = update_track(tle)
                for current_date, subsat_points in tracker:
                    SubsatellitePoint.objects.bulk_create(subsat_points)
                self.stdout.write('\nFinished create and save SubsattellitePoints\n')
            except:
                self.stdout.write('Fail create and save SubsattellitePoints\n')
        else:
            self.stdout.write('Create new SubsatellitePoints aborted. No new TLE.\n')