# coding: utf-8
from datetime import timedelta
from math import degrees

from django.contrib.gis.geos import Point
from ephem import readtle
from tqdm import tqdm

from .models import SubsatellitePoint


def make_key(key, key_prefix, version):
    return '::'.join([key_prefix, str(version), str(key).replace(' ', '_')])


class DateTimeRange(object):
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __len__(self):
        start = self.start.timestamp()
        stop = self.stop.timestamp()
        return int((stop - start) / self.step)

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= self.stop:
            start = self.start
            self.start += timedelta(seconds=self.step)
            return start, self.start
        else:
            raise StopIteration()


class DayRange(DateTimeRange):
    def __init__(self, *args):
        super(DayRange, self).__init__(*args)
        self.step *= 86400

    def __next__(self):
        if self.start < self.stop:
            start = self.start
            self.start += timedelta(seconds=self.step)
            return start, self.start
        else:
            raise StopIteration()


def chunker(chunk_size, iterable):
    count = len(iterable) // chunk_size
    for i in range(count + 1):
        yield iterable[:chunk_size]
        iterable = iterable[chunk_size:]


def get_ISS_subsatpoint(tle, iss_time):
    iss = readtle(tle.title_line, tle.line1, tle.line2)
    iss.compute(iss_time)
    sublong, sublat = map(degrees, (iss.sublong, iss.sublat))
    return iss_time, Point(sublong, sublat)


def update_track(tle, delta=timedelta(days=1), step_in_sec=1):
    start = tle.datetime_in_lines
    stop = start + delta
    SubsatellitePoint.objects.filter(date_time__gte=start).delete()
    iss = readtle(tle.title_line, tle.line1, tle.line2)
    for iss_time, next_time in tqdm(DateTimeRange(start, stop, step_in_sec), leave=True):
        iss.compute(iss_time)
        sublong, sublat = map(degrees, (iss.sublong, iss.sublat))
        # yield SubsatellitePoint(date_time=iss_time, location=Point(sublong, sublat), tle=tle), (iss_time, Point(sublong, sublat))
        yield iss_time, Point(sublong, sublat)
