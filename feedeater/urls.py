from django.conf.urls.defaults import patterns, include, url

from feedeater.models import Feed, Entry

urlpatterns = patterns('',
    url(r'^$', 'feedeater.views.recent_entries', name="application_content"),
    url(r'^recent/$', 'feedeater.views.recent_entries', name="recent_entries"),
    url(r'^search/$', 'feedeater.views.search', name="search"),
    url(r'^search/ajax/$', 'feedeater.views.search_ajax', name="search_ajax"),
)
