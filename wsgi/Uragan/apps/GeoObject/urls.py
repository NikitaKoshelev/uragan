from django.conf.urls import patterns, url
from .views import DetailGeoObject, where_iss, WizardCreateGeoObject, get_kml


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'UraganUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^create/$', CreateGeoObject.as_view()),
    url(r'^detail/(?P<pk>\d+)', DetailGeoObject.as_view(), name='detail'),
    url(r'^kml/(?P<pk>\d+)', get_kml, name='get_kml'),
    url(r'^create/$', WizardCreateGeoObject.as_view()),
    url(r'^where_iss/$', where_iss),
)
