from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted_at'
    fields = (
    'title',
    'slug',
    'description',
    'code_language',
    'code',
    'link_desc',
    'link_path',
    'binary_desc',
    'binary_path'
    )
    list_display = ['title', 'updated_at']
    list_display_links = ['title']
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Post, PostAdmin)