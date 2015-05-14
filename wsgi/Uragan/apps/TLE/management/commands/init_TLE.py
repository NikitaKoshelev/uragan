# coding: utf-8

from django.core.management.base import BaseCommand
from apps.TLE.models import TLE, Satellite
from apps.TLE import spacetrack
from datetime import date
from dateutil.parser import parse
from tqdm import tqdm


def unique_tle(seq, satellite):

    seen = set()
    seen_add = seen.add
    for tle in tqdm(seq, leave=True):

        datetime_in_lines = parse('{}.{} {}'.format(tle['EPOCH'], tle['EPOCH_MICROSECONDS'], 'UTC'))
        norad_id = tle['NORAD_CAT_ID']

        if not ((datetime_in_lines, norad_id) in seen or seen_add((datetime_in_lines, norad_id))):
            title_line = '{:<24}'.format(tle['TLE_LINE0'][2:].strip())
            line1 = '{:<69}'.format(tle['TLE_LINE1'].strip())
            line2 = '{:<69}'.format(tle['TLE_LINE2'].strip())

            yield TLE(title_line=title_line, line1=line1, line2=line2,
                      datetime_in_lines=datetime_in_lines, satellite=satellite)

    del seq, seen


class Command(BaseCommand):
    help = 'Download TLE files'

    def handle(self, **options):
        TLE.objects.all().delete()
        satellites = Satellite.objects.all()

        for sat in satellites:
            try:
                credentials = {'identity': 'nikita.koshelev@gmail.com', 'password': 'K0SHeLeV21101994'}
                query = spacetrack.tle_query_build(date_range=(date(1998, 11, 20), date.today()),
                                                   norad_id=str(sat.satellite_number), sort='asc')

                self.stdout.write('Start download object - ' + sat.title)
                r = spacetrack.request_sequence(credentials, spacetrack_query=query)
                self.stdout.write('Finished download object - ' + sat.title)

                self.stdout.write('Start create and save object - ' + sat.title)
                TLE.objects.bulk_create(unique_tle(r, sat))
                self.stdout.write('\nFinished create and save object - ' + sat.title)
            except:
                self.stdout.write('Fail download, create or save object - ' + sat.title)
