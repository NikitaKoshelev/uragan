from django.conf.urls import patterns, url
from .views import TLE_ListView, TLEDayArchiveView, TLETodayArchiveView
from .api import satellites_list, tle

urlpatterns = (
    url(r'^$', TLE_ListView.as_view(), name='list'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', TLEDayArchiveView.as_view(), name="archive_day"),
    url(r'^today/$', TLETodayArchiveView.as_view(), name="today"),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/satellite_list$', satellites_list),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/tle', tle),
)
