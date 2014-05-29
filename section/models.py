from django.db import models

class Section(models.Model):
    """Section Page"""
    title = models.CharField(max_length=255)
    sort_key = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, blank=True)
    blurb = models.TextField(blank=True)
    nav = models.BooleanField()
    
    class Meta:
        ordering = ['sort_key', 'title']
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Section, self).save(*args, **kwargs)


class Slice(models.Model):
    """Container for Grid blocks"""
    section = models.ForeignKey(Section)
    sort_key = models.IntegerField(default=0)
    title = models.CharField(max_length=225, blank=True)
    
    class Meta:
        ordering = ['sort_key']
    
    def __unicode__(self):
        return '{0}: {1} ({2})'.format(self.section, self.sort_key, self.title)
        

class Grid(models.Model):
    """"define grid-size choices"""
    GRID_CHOICES = (
        ('full', 'Full'),
        ('half', 'Half'),
        ('third', 'Third'),
        ('two-thirds','Two-Thirds'),
        ('quarter', 'Quarter'),
    )
    
    slice = models.ForeignKey(Slice)
    size = models.CharField(max_length=10, choices=GRID_CHOICES)
    sort_key = models.IntegerField(default=0)
    header = models.CharField(max_length=255, blank=True)
    # holds content, or image title text
    content = models.TextField(blank=True)
    # if anything, it's code
    language = models.CharField(max_length=16, blank=True)
    # if anything, it's an img
    img = models.FileField(upload_to='section/img', blank=True)
    
    class Meta:
        ordering = ['slice__section__title', 'slice__sort_key', 'sort_key']
    
    def __unicode__(self):
        return '{0}-{1}'.format(self.slice, self.sort_key)


class Link(models.Model):
    grid = models.ForeignKey(Grid)
    # the text to display as a link
    display = models.CharField(max_length=255)
    # a contact me link
    contact_link = models.BooleanField()
    # a link to another section
    section_link = models.ForeignKey(Section, null=True, blank=True)
    # a url link
    other_link = models.CharField(max_length=225, blank=True)
    # an uploaded file
    file_link = models.FileField(upload_to='section/bin', blank=True)

    class Meta:
        ordering = ['grid__slice__section__title', 'grid__slice__sort_key',
                    'grid__sort_key', 'display']
    
    def __unicode__(self):
        return '{0}> {1}'.format(self.grid, self.display)