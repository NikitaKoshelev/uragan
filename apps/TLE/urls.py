from django.conf.urls import url

from .api import satellites_list, tle
from .views import SatelliteDetailView, SatelliteListView
from .views import TLE_ListView, TLEDayArchiveView, TLETodayArchiveView, point_from_datetime

urlpatterns = [
    url(r'^$', TLE_ListView.as_view(), name='list'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', TLEDayArchiveView.as_view(),
        name='archive_day'),
    url(r'^point/(?P<date>[0-9\-]+)/(?P<time>[0-9\-]+)/$', point_from_datetime, name='point'),
    url(r'^today/$', TLETodayArchiveView.as_view(), name="today"),
]

urlpatterns += [
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/satellite_list$', satellites_list),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/tle', tle),
]

urlpatterns += [
    url(r'^sattellites/$', SatelliteListView.as_view(), name='satellites_list'),
    url(r'^sattellite/detail/(?P<pk>\d+)/$', SatelliteDetailView.as_view(), name='satellite'),
]
