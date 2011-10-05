from django.conf.urls.defaults import patterns, include, url

from snippets.models import Snippet

urlpatterns = patterns('',
    url(r'^$', 'snippets.views.random_snippet', name='random_snippet'),
)
