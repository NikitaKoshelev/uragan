from django.conf.urls import patterns, url
from .views import TLE_ListView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UraganUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TLE_ListView.as_view()),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/satellite_list$', 'TLE.api.satellites_list'),
    url(r'^api/(?P<fmt>[a-zA-Z]{3,4})/tle', 'TLE.api.tle'),
)
