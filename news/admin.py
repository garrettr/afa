from django.contrib import admin
from news.models import Post

from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.admin.item_editor import FeinCMSInline

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('media_files',)
    raw_id_fields = ('photo', )
    list_display = ('headline', 'start_date', 'end_date', 'visible', )
    list_filter = ('start_date',)
    prepopulated_fields = {'slug': ('headline',)}
    search_fields = ('title', 'slug', 'body', )
    list_per_page = 10

    fieldsets = (
        (None, {
            'fields': (('headline', 'visible'), 'slug', )
        }),
        ('Event details', {
            'fields': ('start_date', 'end_date', 'location', )
        }),
        ('Description', {
            'fields': ('body', 'photo', 'media_files'),
            'classes': ('collapse',),
        }),
    )

    class Media:
        js = (
            "/static/js/tiny_mce/tiny_mce.js",
            "/static/js/admin_tinymce.js",
        )

admin.site.register(Post, PostAdmin)
