from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fields = ("published", "title", 'slug', 'author', "content")
    list_display = ['published', "title", 'author', "updated_at"]
    list_display_links = ['title']
    list_editable = ['published']
    list_filter = ['author', "published", "updated_at"]
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Post, PostAdmin)