from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.application.models import ApplicationContent

Page.register_templates({
    'key': 'base',
    'title': 'Base Template',
    'path': 'base.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    })

Page.create_content_type(RichTextContent)
MediaFileContent.default_create_content_type(Page)
Page.create_content_type(RawContent)
Page.create_content_type(ImageContent, POSITION_CHOICES=(
    ('block', _('block')),
    ('left', _('left')),
    ('right', _('right')),
    ))

from django.db import models
from django.template.loader import render_to_string
from photologue.models import Gallery, Photo, PhotoSize

class PhotoContent(models.Model):
    '''
    A single photo from a Photologue gallery
    '''
    photo = models.ForeignKey(Photo, verbose_name=_(u'Photo'))
    size = models.ForeignKey(PhotoSize, verbose_name=_(u'Size'))

    class Meta:
        abstract = True
        verbose_name = _(u'Photo')
        verbose_name_plural = _(u'Photos')

    def render(self, **kwargs):
        photosize = self.size

        if not self.photo.size_exists(photosize):
            self.photo.create_size(photosize)
        if photosize.increment_count:
            self.photo.increment_count()
        url_for_size = '/'.join([
            self.photo.cache_url(),
            self.photo._get_filename_for_size(photosize.name)
        ])

        return render_to_string('photologue/photo_content.html',
                {
                    'photo': self.photo,
                    'url_for_size': url_for_size,
                })

class GalleryContent(models.Model):
    gallery = models.ForeignKey(Gallery, verbose_name=_(u'Gallery'))

    class Meta:
        abstract = True
        verbose_name = _(u'Gallery')
        verbose_name_plural = _(u'Galleries')

    def render(self, **kwargs):
        return render_to_string('photologue/gallery_embed.html',
                {
                    'gallery': self.gallery
                }
            )

Page.create_content_type(PhotoContent)
Page.create_content_type(GalleryContent)
