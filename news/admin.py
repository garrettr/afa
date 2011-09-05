from django.contrib import admin
from news.models import Post

from feincms.module.medialibrary.models import MediaFile
from feincms.module.medialibrary.fields import MediaFileForeignKey
from feincms.admin.item_editor import FeinCMSInline

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('media_files',)
    raw_id_fields = ('photo', )
    list_display = ('pub_date', 'headline', 'photo', )
    list_display_links = ('headline', )
    list_filter = ('pub_date',)
    prepopulated_fields = {'slug': ('headline',)}
    search_fields = ('title', 'slug', 'body', )
    list_per_page = 10

admin.site.register(Post, PostAdmin)
