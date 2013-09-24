from django.db import models

class Section(models.Model):
    '''Section Page'''
    title = models.CharField(max_length=255)
    sort_key = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, blank=True)
    blurb = models.TextField(blank=True)
    
    class Meta:
        ordering = ['sort_key','title']
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Section, self).save(*args, **kwargs)

class Slice(models.Model):
    '''Contianer for Grid blocks'''
    section = models.ForeignKey(Section)
    sort_key = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_key']
    
    def __unicode__(self):
        return '{0}: {1}'.format(self.section, self.sort_key)
        

class Grid(models.Model):
    # define grid-size choices
    GRID_CHOICES = (
        ('full', 'Full'),
        ('half', 'Half'),
        ('third', 'Third'),
        ('quarter', 'Quarter'),
    )
    
    slice = models.ForeignKey(Slice)
    size = models.CharField(max_length=7, choices=GRID_CHOICES)
    sort_key = models.IntegerField(default=0)
    header = models.CharField(max_length=255, blank=True)
    # holds content, or image title text
    content = models.TextField(blank=True)
    # if anything, it's code
    language = models.CharField(max_length=16, blank=True)
    # if anything, it's an img
    img = models.ImageField(upload_to='section/img', blank=True)
    
    class Meta:
        ordering = ['sort_key']
    
    def __unicode__(self):
        return '{0}-{1}'.format(self.slice, self.sort_key)