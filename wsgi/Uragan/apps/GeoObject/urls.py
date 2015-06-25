from django.conf.urls import patterns, url
from .views import DetailGeoObject, where_iss, WizardCreateGeoObject, ListGeoObject, UpdateGeoObject
from .api import get_kml_by_title, get_kml_by_object, geocoder


# Views
urlpatterns = [
    url(r'^list/$', ListGeoObject.as_view(), name='list'),
    url(r'^detail/(?P<pk>\d+)/$', DetailGeoObject.as_view(), name='detail'),
    url(r'^create/$', WizardCreateGeoObject.as_view(), name='create'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateGeoObject.as_view(), name='create'),
    url(r'^where_iss/$', where_iss),
]


# API
urlpatterns += [
    url(r'^api/geocoder/$', geocoder, name='geocoder'),
    url(r'^api/geocoder/(?P<lang>[a-zA-z]{2})/$', geocoder, name='geocoder_with_lang'),
    url(r'^kml/(?P<pk>\d+)/$', get_kml_by_object, name='get_kml_by_object'),
    url(r'^kml/$', get_kml_by_title, name='get_kml_by_title'),
]
