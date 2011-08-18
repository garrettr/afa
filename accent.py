from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms._internal import monkeypatch_property

from feincms.content.medialibrary.v2 import MediaFileContent
from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.admin.item_editor import FeinCMSInline
from afa.models import ImageContentInline

from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ColorWidget(forms.TextInput):
    
    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''
        <style>
        #id_%s { background: white; font: 16px Courier, monospace; }
        </style>
            <script type="text/javascript">
            $(document).ready(function() {
                $('#id_%s').css("background", $('#id_%s').val());
                $('#id_%s').keyup(function() {
                    $(this).css("background", $(this).val());
                });
            });
            </script>''' % (name, name, name, name) )

class ColorField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)

def register(cls, admin_cls):
    cls.add_to_class('_content_title', models.TextField(_('content title'), blank=True,
        help_text=_('The first line is the main title, the following lines are subtitles.')))
    cls.add_to_class('_header_image', MediaFileForeignKey(MediaFile, blank=True, null=True,
        help_text=_('Link to an image to use for the page header. We recommend resizing it to 960x210 so there are no surprises.')))
    cls.add_to_class('_accent_color', ColorField(_('accent color'), blank=True,
        default="#A2E663",
        help_text=_('Accent color (in hex): used for navigation tabs and links')))

    # Ask matthias about this
    feincms_item_editor_inline = ImageContentInline

    cls.add_to_class('feincms_item_editor_inline', feincms_item_editor_inline)

    @monkeypatch_property(cls)
    def content_title(self):
        """
        This should be used f.e. for the <h1>-tag
        """

        if not self._content_title:
            return self.title

        return self._content_title.splitlines()[0]

    @monkeypatch_property(cls)
    def content_subtitle(self):
        return mark_safe(u'<br />'.join(self._content_title.splitlines()[1:]))

    @monkeypatch_property(cls)
    def header_image(self):
        return self._header_image.file

    @monkeypatch_property(cls)
    def accent_color(self):
        return self._accent_color

    admin_cls.fieldsets.append((_('Accent'), {
        'fields': ('_content_title', '_header_image', '_accent_color',),
        'classes': ('collapse',),
        }))
