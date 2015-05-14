from django.conf.urls import patterns, url
from .views import CreateGeoObject, CreateGeoObjectPart1, where_iss


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UraganUI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^create/$', CreateGeoObject.as_view()),
    url(r'^create/partition/part_1/$', CreateGeoObjectPart1.as_view()),
    url(r'^create/partition/part_2/$', CreateGeoObject.as_view()),
    url(r'^where_iss/$', where_iss),
)
