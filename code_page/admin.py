from django.contrib import admin
from .models import Code_Page

class Code_PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted_at'
    fields = ('title', 'slug', 'description', 'code', 'link', 'binary_path')
    list_display = ['title', 'updated_at']
    list_display_links = ['title']
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Code_Page, Code_PageAdmin)