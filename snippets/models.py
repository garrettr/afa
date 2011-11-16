from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey

class Snippet(models.Model):
    '''
    A helpful bit of text to point people to some of the different resources on
    the new website. Appears on the homepage under the header.
    '''
    title = models.CharField(_(u'title'), max_length=200)
    url = models.CharField(_(u'url'), max_length=255, blank=True,
            help_text=_('Optional: Link to a related website'))
    body = models.TextField(_(u'body'))
    photo = MediaFileForeignKey(MediaFile, blank=True, null=True, 
            help_text=_('Optional: Pick a snapshot to go along with this post. Will be resized to fit'))

    def __unicode__(self):
        return u'%s' % self.title
