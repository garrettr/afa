from django.conf.urls.defaults import patterns, include, url

from news.models import Post

# p. 73 of PDP
post_info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'pub_date',
    }

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', post_info_dict,
        'news_post_archive_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', post_info_dict,
        'news_post_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', post_info_dict,
        'news_post_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', post_info_dict,
        'news_post_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'object_detail', post_info_dict,
        'news_post_detail'),
)
