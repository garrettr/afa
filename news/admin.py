from django.contrib import admin
from news.models import Post

class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('photo',)
    list_display = ('pub_date', 'headline', 'photo', )
    list_display_links = ('headline', )
    list_filter = ('pub_date',)
    search_fields = ('title', 'slug', 'body', )
    list_per_page = 10

admin.site.register(Post, PostAdmin)
