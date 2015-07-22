# coding: utf-8

from datetime import datetime, timedelta
from tqdm import tqdm
from pytz import utc

from django.core.management.base import BaseCommand
from apps.TLE.models import TLE, Satellite


def unique_tle(lines, satellite):
    title = satellite.title
    norad_id = satellite.satellite_number
    seen = set(satellite.tle_set.values_list('datetime_in_lines', 'satellite'))

    len_lines = len(lines)
    for line1, line2 in zip(lines[1:len_lines:3], lines[2:len_lines:3]):
        year = int(line1[18:20])
        year += 2000 if year < 90 else 1900
        datetime_in_lines = datetime(year, 1, 1, 0, 0, 0, 0, utc) + timedelta(days=float(line1[20:32]) - 1)

        if not (datetime_in_lines, norad_id) in seen:
            seen.add((datetime_in_lines, norad_id))

            title_line = '{:<24}'.format(title.strip())
            line1 = '{:<69}'.format(line1.strip())
            line2 = '{:<69}'.format(line2.strip())

            yield TLE(title_line=title_line, line1=line1, line2=line2,
                      datetime_in_lines=datetime_in_lines, satellite=satellite)

    del lines, seen


class Command(BaseCommand):
    help = 'Download TLE files'

    def handle(self, **options):
        fh = open('3le.txt', 'r', encoding='utf8')
        lines = fh.readlines()
        fh.close()
        title = lines[0][2:].strip()
        norad_id = int(lines[1][2:7])
        sat, status = Satellite.objects.get_or_create(title=title, satellite_number=norad_id)
        if not status:
            sat.tle_set.all().delete()
        try:
            self.stdout.write('Start create and save object - ' + sat.title + '\n')
            TLE.objects.bulk_create(unique_tle(lines, sat))
            self.stdout.write('Finished create and save object - ' + sat.title + '\n')
        except:
            self.stdout.write('Fail create and save object - ' + sat.title + '\n')
