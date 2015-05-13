from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from solid_i18n.urls import solid_i18n_patterns

js_info_dict = {
    'packages': ('common',),
}

urlpatterns = solid_i18n_patterns(
    '',
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^geo-object/', include('apps.GeoObject.urls'), name='GeoObject'),
    url(r'^TLE/', include('apps.TLE.urls'), name='TLE'),
)

urlpatterns += patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^select2/', include('django_select2.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='js_catalog'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
