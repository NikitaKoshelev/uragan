from django.conf.urls import url

from .api import get_kml_by_title, get_kml_by_object_id, geocoder
from .views import CreateSurveillancePlan, DetailSurveillancePlan, UpdateSurveillancePlan, ListSurveillancePlan
from .views import DetailGeoObject, where_iss, WizardCreateGeoObject, ListGeoObject, UpdateGeoObject, CreateGeoObject

# Views GeoObject
urlpatterns = [
    url(r'^$', ListGeoObject.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', DetailGeoObject.as_view(), name='detail'),
    url(r'^create/wizard/$', WizardCreateGeoObject.as_view(), name='create'),
    url(r'^create/$', CreateGeoObject.as_view(), name='create_full'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateGeoObject.as_view(), name='edit'),
    url(r'^where_iss/$', where_iss),
]

# API GeoObject
urlpatterns += [
    url(r'^api/geocoder/$', geocoder, name='geocoder'),
    url(r'^api/geocoder/(?P<lang>[a-zA-z]{2})/$', geocoder, name='geocoder_with_lang'),
    url(r'^kml/(?P<pk>\d+)/$', get_kml_by_object_id, name='get_kml_by_object'),
    url(r'^kml/$', get_kml_by_title, name='get_kml_by_title'),
]

# Views SurveillancePlan
urlpatterns += [
    url(r'^surveillance-plan/$', ListSurveillancePlan.as_view(), name='plans_list'),
    url(r'^surveillance-plan/(?P<pk>\d+)/$', DetailSurveillancePlan.as_view(), name='detail_plan'),
    url(r'^surveillance-plan/create/$', CreateSurveillancePlan.as_view(), name='create_plan'),
    url(r'^surveillance-plan/edit/(?P<pk>\d+)/$', UpdateSurveillancePlan.as_view(), name='edit_plan'),
]
