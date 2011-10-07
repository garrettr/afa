from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.v2 import MediaFileContent
from feincms.content.section.models import SectionContent
from feincms.content.table.models import TableContent
from feincms.content.application.models import ApplicationContent

Page.register_templates(
    {
    'key': '2col',
    'title': 'Two Column',
    'path': '2col.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    },
    {
    'key': 'fullpage',
    'title': 'Full Page',
    'path': 'fullpage.html',
    'regions': (
        ('main', 'Main region'),
    )
    },
    {
    'key': 'home',
    'title': 'Home',
    'path': 'home.html',
    'regions': (
        ('subhead', 'Under Header'),
        ('news', 'News'),
        ('calendar', 'Calendar'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    },
    {
    'key': 'alliance-ourmission',
    'title': 'The Alliance -> Our Mission',
    'path': 'alliance-ourmission.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'alliance-howwework',
    'title': 'The Alliance -> How We Work',
    'path': 'alliance-howwework.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'alliance-partnergroups',
    'title': 'The Alliance -> Partner Groups',
    'path': 'alliance-partnergroups.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar'),
        ),
    },
    {
    'key': 'alliance-history',
    'title': 'The Alliance -> History',
    'path': 'alliance-history.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'background-whatismtr',
    'title': 'Background -> What is MTR?',
    'path': 'background-whatismtr.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'background-whatisappalachia',
    'title': 'Background -> What is Appalachia?',
    'path': 'background-whatisappalachia.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'resources-printablematerials',
    'title': 'Resources -> Printable Materials', 
    'path': 'resources-printablematerials.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'resources-images',
    'title': 'Resources -> Images', 
    'path': 'resources-images.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'resources-links',
    'title': 'Resources -> Links', 
    'path': 'resources-links.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'resources-powerpointpresentations',
    'title': 'Resources -> Powerpoint Presentations', 
    'path': 'resources-powerpointpresentations.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'donate',
    'title': 'Donate',
    'path': 'donate.html',
    'regions': (
        ('main', 'Main region'),
        ),
    },
)

Page.create_content_type(RichTextContent)
Page.create_content_type(SectionContent, 
        TYPE_CHOICES = (
            ('block', _(u'block')),
            ('imageleft', _(u'image (left)')),
            ('imageright', _(u' image (right)')),
        )
    )

from django.db import models
from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.admin.item_editor import FeinCMSInline
from django.template.loader import render_to_string

class ImageContentInline(FeinCMSInline):
    raw_id_fields = ('image',)

class ImageContent(models.Model):
    feincms_item_editor_inline = ImageContentInline

    image = MediaFileForeignKey(MediaFile)
    caption = models.TextField(blank=True)
    link = models.URLField(max_length=200, blank=True,
            help_text=_(u'Leave blank for no link'))

    SIZE_CHOICES = (
        # based on 960.gs
        (u'80x80', u'thumbnail'),
        (u'220x9999', u'small'),
        (u'300x9999', u'medium'),
        (u'460x9999', u'large'),
    )

    # do alignment as well
    size = models.CharField(max_length=9, choices=SIZE_CHOICES, blank=True,
            null=True,
            help_text=_(u'Leave blank to use original image size'))

    ALIGN_CHOICES = (
        (0, u'Center (block)'),
        (1, u'Left'),
        (2, u'Right'),
    )
    align = models.IntegerField(choices=ALIGN_CHOICES, default=0)

    class Meta:
        abstract = True
        verbose_name = _(u'Image')

    def render(self, **kwargs):
        return render_to_string('content/image.html',
                {
                    'image': self.image,
                    'caption': self.caption,
                    'link': self.link,
                    'size': self.size,
                    'align': self.align,
                }
            )

Page.create_content_type(ImageContent)

class GalleryContent(models.Model):

    title = models.CharField(max_length=200)
    images = models.ManyToManyField(MediaFile)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name = _(u'Gallery')
        verbose_name_plural = _(u'Galleries')

    def render(self, **kwargs):
        return render_to_string('gallery/gallery.html',
                {
                    'title': self.title,
                    'images': self.images.all(),
                }
            )


Page.create_content_type(GalleryContent)

Page.create_content_type(RawContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('Default')),
    ))

Page.register_extensions('accent',)

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('news.urls', 'News'),
    ('snippets.urls', 'Snippets'),
))
