from django.conf.urls import patterns, url
from .views import CreateGeoObject, where_iss, WizardCreateGeoObject


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UraganUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^create/$', CreateGeoObject.as_view()),
    url(r'^wizard/$', WizardCreateGeoObject.as_view()),
    url(r'^where_iss/$', where_iss),
)
