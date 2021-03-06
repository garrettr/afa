from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.admin.item_editor import FeinCMSInline

class Post(models.Model):
    headline = models.CharField(_(u'headline'), max_length=100)
    slug = models.SlugField(_(u'slug'), max_length=100)
    visible = models.BooleanField(default=True)
    body = models.TextField(_(u'body'), blank=True) # feincms/tinymce richtext widget
    photo = MediaFileForeignKey(MediaFile, blank=True, null=True, 
            help_text=_('Optional: Pick a snapshot to go along with this post. Will be resized to fit'))

    # optional attachments
    media_files = models.ManyToManyField(MediaFile, related_name='post_mediafiles',
            blank=True, null=True
        )

    # optional event details
    start_date = models.DateField(blank=True, null=True,
            help_text=_('Optional: If this is for an event, when will it start?'))
    end_date = models.DateField(blank=True, null=True,
            help_text=_('Optional: If this is for an event, when will it end?'))
    location = models.CharField(max_length=255, blank=True,
            help_text=_('Optional: If this is for an event, where will it take \
            place? Enter a location that Google Maps can resolve.'))

    # timestamp
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.headline

    @models.permalink
    def get_absolute_url(self):
        return ('news_post_detail', (), {
            'year': self.pub_date.strftime("%Y"),
            'month': self.pub_date.strftime("%b").lower(),
            'day': self.pub_date.strftime("%d"),
            'slug': self.slug
        })
