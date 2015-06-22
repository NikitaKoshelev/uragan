from django.conf.urls import patterns, url
from .views import TLE_ListView
from .api import satellites_list, tle

urlpatterns = (
    url(r'^$', TLE_ListView.as_view(), name='list'),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/satellite_list$', satellites_list),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/tle', tle),
)
