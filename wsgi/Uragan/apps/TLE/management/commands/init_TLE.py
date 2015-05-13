# coding: utf-8

from django.core.management.base import BaseCommand
from apps.TLE.models import TLE, Satellite
from apps.TLE import spacetrack
from datetime import datetime, date, timedelta
from pytz import utc


class Command(BaseCommand):
    help = 'Download TLE files'

    def handle(self, **options):
        TLE.objects.all().delete()
        satellites = Satellite.objects.all()
        satellites_ids = ','.join(map(str, (sat.satellite_number for sat in satellites)))
        credentials = {'identity': 'nikita.koshelev@gmail.com', 'password': 'K0SHeLeV21101994'}
        query = spacetrack.tle_query_build(date_range=(date(2015, 5, 1), date.today()),
                                           norad_id=satellites_ids)
        r = spacetrack.request_sequence(credentials, spacetrack_query=query)
        result = set((datetime.strptime(tle['EPOCH'], '%Y-%m-%d %H:%M:%S'), int(tle['EPOCH_MICROSECONDS']),
                      int(tle['NORAD_CAT_ID']),
                      tle['TLE_LINE0'][2:], tle['TLE_LINE1'], tle['TLE_LINE2']) for tle in r)

        TLE_list = []
        for epoch, epoch_microseconds, satellite_number, title, line1, line2 in result:
            print(epoch, epoch_microseconds, satellite_number, title)
            datetime_in_lines = epoch.replace(tzinfo=utc) + timedelta(microseconds=epoch_microseconds)

            title_line = '{:<24}'.format(title.strip())
            line1 = '{:<69}'.format(line1.strip())
            line2 = '{:<69}'.format(line2.strip())

            TLE_list.append(
                TLE(#datetime_creation=datetime.utcnow(),
                    title_line=title_line,
                    line1=line1,
                    line2=line2,
                    datetime_in_lines=datetime_in_lines,
                    satellite=satellites.get(satellite_number=satellite_number))
                )

        TLE.objects.bulk_create(sorted(TLE_list, key=lambda x: x.datetime_in_lines))

        self.stdout.write('Download finished')
