from django.contrib import admin
from .models import Section, Slice, Grid, Link

class SectionAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'sort_key',
        'slug',
        'blurb',
        'nav'
    )
    list_display = ['title', 'sort_key', 'nav']
    list_display_links = ['title']
    prepopulated_fields = {'slug':('title',)}

class SliceAdmin(admin.ModelAdmin):
    fields = ('section', 'sort_key', 'title')
    
    list_display = ['section', 'sort_key']
    list_display_links = ['sort_key']
    
    list_filter = ('section__title',)

class GridAdmin(admin.ModelAdmin):
    fields = (
        'slice',
        'size',
        'sort_key',
        'header',
        'content',
        'language',
        'img'
    )
    list_display = ['slice', 'sort_key']
    list_display_links = ['sort_key']
    list_filter = ('slice__section__title', 'slice__sort_key')

class LinkAdmin(admin.ModelAdmin):
    fields = (
        'grid',
        'display',
        'section_link',
        'other_link',
        'file_link'
    )
    list_display = ['grid', 'display']
    list_display_links = ['display']
    list_filter = ('grid',)
    
admin.site.register(Section, SectionAdmin) 
admin.site.register(Slice, SliceAdmin)
admin.site.register(Grid, GridAdmin)
admin.site.register(Link, LinkAdmin)
