from django.contrib import admin
from news.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'headline', 'photo', )
    list_display_links = ('headline', )
    search_fields = ('title', 'slug', 'body', )
    list_per_page = 10

admin.site.register(Post, PostAdmin)
