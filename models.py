from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.v2 import MediaFileContent
from feincms.content.section.models import SectionContent
from feincms.content.table.models import TableContent
from feincms.content.application.models import ApplicationContent

Page.register_templates({
    'key': 'base',
    'title': 'Base Template',
    'path': 'base.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    },
    {
    'key': 'main-sidebar',
    'title': 'Main -> Sidebar',
    'path': 'main-sidebar.html',
    'regions': (
        ('main', 'Main region'),
        ('sidebar', 'Sidebar', 'inherited'),
        ),
    },
    {
    'key': 'sidebar-main',
    'title': 'Sidebar -> Main',
    'path': 'sidebar-main.html',
    'regions': (
        ('sidebar', 'Sidebar', 'inherited'),
        ('main', 'Main region'),
        ),
    },
    {
    'key': 'three-col',
    'title': 'Three Column',
    'path': '3col.html',
    'regions': (
        ('leftcol', 'Left Column'),
        ('centercol', 'Center Column'),
        ('rightcol', 'Right Column'),
        )
    },
)

Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('Default')),
    ))
Page.create_content_type(SectionContent, TYPE_CHOICES=(
    ('default', _("Default")),
    ))

Page.register_extensions('accent',)
