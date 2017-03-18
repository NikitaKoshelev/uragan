# coding: utf-8

import os
import sys
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

from django.core.management.base import BaseCommand
from requests import get

from apps.TLE.models import TLE, Satellite
from .init_TLE_ISS_formfile import unique_tle

if sys.version_info.major == 2:
    from urllib import urlretrieve  # python 2.x
else:
    from urllib.request import urlretrieve  # python 3.x


class Command(BaseCommand):
    help = 'Download TLE files'

    def handle(self, **options):
        count = TLE.objects.count()

        if count:
            last_TLE = TLE.objects.first()
            last_mktime = mktime_tz(parsedate_tz(last_TLE.datetime_in_lines.ctime()))
        else:
            last_mktime = 0

        url = 'http://www.celestrak.com/NORAD/elements/stations.txt'

        resp = get(url)

        url_mktime = mktime_tz(parsedate_tz(resp.headers['last-modified']))
        url_datetime = datetime.utcfromtimestamp(url_mktime)
        if url_mktime > last_mktime:
            self.stdout.write('Date and time of creation TLE: {}'.format(url_datetime.isoformat()))
            self.stdout.write('New TLE found, downloading...')

            result = urlretrieve(url, 'TLE.txt')
            fh = open(result[0], 'r', encoding='utf8')
            lines = fh.readlines()[:3]
            fh.close()
            os.remove(result[0])
            title = lines[0].strip()
            norad_id = int(lines[1][2:7])
            sat, status = Satellite.objects.get_or_create(title=title, satellite_number=norad_id)
            try:
                self.stdout.write('Start create and save object - ' + sat.title + '\n')
                TLE.objects.bulk_create(unique_tle(lines, sat))
                self.stdout.write('Finished create and save object - ' + sat.title + '\n')
            except:
                self.stdout.write('Fail create and save object - ' + sat.title + '\n')
        else:
            self.stdout.write('No new TLE. A new attempt after 5 minutes...')
