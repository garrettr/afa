from django.contrib import admin
from feedeater.models import Feed, Entry

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'source', 'created_on')
    search_fields = ('title', 'url', 'source')
    list_filter = ('source', )

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_on', 'feed',)
    search_fields = ('title', 'url', 'description', )
    list_filter = ('feed', 'feed__source',)
    list_per_page = 25

admin.site.register(Feed, FeedAdmin)
admin.site.register(Entry, EntryAdmin)
