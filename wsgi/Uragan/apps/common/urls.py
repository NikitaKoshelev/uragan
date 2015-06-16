from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from solid_i18n.urls import solid_i18n_patterns
from .views import translate_string
js_info_dict = {
    # 'packages': ('apps.common',),
}

urlpatterns = solid_i18n_patterns(
    '',
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='accounts')),
    url(r'^geo-object/', include('apps.GeoObject.urls', namespace='GeoObject')),
    url(r'^TLE/', include('apps.TLE.urls', namespace='TLE')),
    url(r'^translate/$', translate_string),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

)

urlpatterns += patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^select2/', include('django_select2.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
