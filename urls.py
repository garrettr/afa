from django.conf.urls.defaults import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'afa.views.home', name='home'),
    # url(r'^afa/', include('afa.foo.urls')),

    # photologue
    url(r'^photologue/', include('photologue.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # serve media - DEVELOPMENT ONLY
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'media/')}),

    # feincms
    url(r'', include('feincms.urls')),

)
