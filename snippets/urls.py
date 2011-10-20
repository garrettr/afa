from django.conf.urls.defaults import patterns, include, url

from snippets.models import Snippet

urlpatterns = patterns('',
    url(r'^$', 'snippets.views.all_as_gallery', name='all_as_gallery'),
)
