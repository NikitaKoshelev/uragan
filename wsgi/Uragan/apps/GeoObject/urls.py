from django.conf.urls import patterns, url
from .views import CreateGeoObject


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UraganUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', CreateGeoObject.as_view()),
)
