# coding: utf-8

import sys
import os

from requests import get
from datetime import datetime, timedelta
from email.utils import parsedate_tz, mktime_tz
from pytz import utc

from django.core.management.base import BaseCommand
from apps.TLE.models import TLE, Satellite

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
            last_mktime = mktime_tz(parsedate_tz(last_TLE.datetime_created.ctime()))
        else:
            last_mktime = 0

        url = 'http://www.celestrak.com/NORAD/elements/stations.txt'

        resp = get(url)

        url_mktime = mktime_tz(parsedate_tz(resp.headers['last-modified']))
        url_datetime = datetime.utcfromtimestamp(url_mktime)

        if url_mktime > last_mktime:
            self.stdout.write('Date and time of creation TLE: {}'.format(url_datetime.isoformat()))
            self.stdout.write('New TLE found, downloading...')

            result = urlretrieve(url, 'TLE.txt'.format(url_mktime))

            fh = open(result[0], 'r', encoding='utf8')
            lines = fh.readlines()
            fh.close()
            os.remove(result[0])

            len_lines = len(lines)
            TLE_list = []
            for title, line1, line2 in zip(lines[::3], lines[1:len_lines:3], lines[2:len_lines:3]):
                year = int('20' + line1[18:20])
                datetime_created = url_datetime.replace(tzinfo=utc)
                datetime_in_lines = datetime(year, 1, 1, 0, 0, 0, 0, utc) + timedelta(days=float(line1[20:32]) - 1)
                satellite_number = line1[2:7]

                sat = Satellite.objects.get_or_create(title=title.strip(), satellite_number=satellite_number)[0]

                title_line = '{:<24}'.format(title.strip())
                line1 = '{:<69}'.format(line1.strip())
                line2 = '{:<69}'.format(line2.strip())

                if sat.tle_set.first():
                    if datetime_in_lines != sat.tle_set.first().datetime_in_lines:
                        TLE_list.append(TLE(datetime_created=datetime_created,
                                            title_line=title_line,
                                            line1=line1,
                                            line2=line2,
                                            datetime_in_lines=datetime_in_lines,
                                            satellite=sat)
                                        )
                else:
                    TLE_list.append(TLE(datetime_created=datetime_created,
                                            title_line=title_line,
                                            line1=line1,
                                            line2=line2,
                                            datetime_in_lines=datetime_in_lines,
                                            satellite=sat)
                                        )

            TLE.objects.bulk_create(TLE_list)

            self.stdout.write('Download finished')
        else:
            self.stdout.write('No new TLE. A new attempt after 5 minutes...')
