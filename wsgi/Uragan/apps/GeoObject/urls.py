from django.conf.urls import patterns, url
from .views import DetailGeoObject, where_iss, WizardCreateGeoObject


urlpatterns = patterns(
    '',
    url(r'^detail/(?P<pk>\d+)', DetailGeoObject.as_view(), name='detail'),
    url(r'^create/$', WizardCreateGeoObject.as_view(), name='create'),
    url(r'^where_iss/$', where_iss),
)


urlpatterns += patterns(
    'apps.GeoObject.api',
    url(r'^api/geocoder/$', 'geocoder', name='geocoder'),
    url(r'^api/geocoder/(?P<lang>[a-zA-z]{2})/$', 'geocoder', name='geocoder_with_lang'),
    url(r'^kml/(?P<pk>\d+)', 'get_kml', name='get_kml'),
)