from django.contrib import admin
from .models import Section, Slice, Grid

class SectionAdmin(admin.ModelAdmin):
    fields = (
    'title',
    'sort_key',
    'slug',
    'blurb'
    )
    list_display = ['title', 'sort_key']
    list_display_links = ['title']
    prepopulated_fields = {'slug':('title',)}

class SliceAdmin(admin.ModelAdmin):
    fields = ('section', 'sort_key')
    
    list_display = ['section', 'sort_key']
    list_display_links = ['sort_key']
    
    list_filter = ('section__title',)

class GridAdmin(admin.ModelAdmin):
    fields= (
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
    
admin.site.register(Section, SectionAdmin) 
admin.site.register(Slice, SliceAdmin)
admin.site.register(Grid, GridAdmin)