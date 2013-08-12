from .models import Post
from django.views.generic import ListView, DetailView

class PublishedPostsMixin(object):
    '''override the queryset'''
    def get_queryset(self):
        return self.model.objects.live()

class PostListView(PublishedPostsMixin, ListView):
    model = Post

class PostDetailView(PublishedPostsMixin, DetailView):
    model = Post