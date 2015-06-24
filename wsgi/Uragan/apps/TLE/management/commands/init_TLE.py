# coding: utf-8

from django.core.management.base import BaseCommand
from apps.TLE.models import TLE, Satellite
from apps.TLE import spacetrack
from datetime import date, timedelta
from dateutil.parser import parse
from tqdm import tqdm
from pytz import utc

def unique_tle(seq, satellite, start):
    seen = set(satellite.tle_set.filter(datetime_in_lines__gte=start).values_list('datetime_in_lines', 'satellite'))
    seen_add = seen.add

    for tle in tqdm(seq, leave=True):

        datetime_in_lines = parse('{}.{}'.format(tle['EPOCH'], tle['EPOCH_MICROSECONDS'])).replace(tzinfo=utc)
        norad_id = int(tle['NORAD_CAT_ID'])

        if not (datetime_in_lines, norad_id) in seen:
            seen_add((datetime_in_lines, norad_id))

            title_line = '{:<24}'.format(tle['TLE_LINE0'][2:].strip())
            line1 = '{:<69}'.format(tle['TLE_LINE1'].strip())
            line2 = '{:<69}'.format(tle['TLE_LINE2'].strip())

            yield TLE(title_line=title_line, line1=line1, line2=line2,
                      datetime_in_lines=datetime_in_lines, satellite=satellite)

    del seq, seen


class Command(BaseCommand):
    help = 'Download TLE files'

    def handle(self, **options):
        #TLE.objects.all().delete()
        satellites = Satellite.objects.all()

        for sat in satellites:
            try:
                credentials = {'identity': 'nikita.koshelev@gmail.com', 'password': 'K0SHeLeV21101994'}
                first_tle = sat.tle_set.first()
                date_start = first_tle.datetime_in_lines.date() if first_tle else date(1998, 11, 20)
                query = spacetrack.tle_query_build(date_range=(date_start, date.today()+timedelta(days=1)),
                                                   norad_id=str(sat.satellite_number), sort='asc')

                self.stdout.write('Start download object - ' + sat.title)
                r = spacetrack.request_sequence(credentials, spacetrack_query=query)
                self.stdout.write('Finished download object - ' + sat.title)

                self.stdout.write('Start create and save object - ' + sat.title)
                TLE.objects.bulk_create(unique_tle(r, sat, date_start))
                self.stdout.write('\nFinished create and save object - ' + sat.title)
            except:
                self.stdout.write('Fail download, create or save object - ' + sat.title)
