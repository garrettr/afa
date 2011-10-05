from django.contrib import admin
from snippets.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    raw_id_fields = ('photo', )
    
    class Media:
        js = (
            "/static/js/tiny_mce/tiny_mce.js",
            "/static/js/admin_tinymce.js",
        )

admin.site.register(Snippet, SnippetAdmin)
