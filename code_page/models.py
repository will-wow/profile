from django.db import models

class Post(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    description = models.TextField()
    code_language = models.CharField(max_length=255, blank=True)
    code = models.TextField(blank=True)
    link_desc = models.CharField(max_length=255, blank=True)
    link_path = models.URLField(max_length=200, blank=True)
    binary_desc = models.CharField(max_length=255, blank=True)
    binary_path = models.FileField(upload_to='code_page/bin', blank=True)
    #image_title = models.CharField(max_length=255)
    #image_path = models.ImageField(upload_to='code_page/img', blank=True)
    
    class Meta:
        ordering = ["-posted_at"]
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('code_page:detail', (), {'slug': self.slug})