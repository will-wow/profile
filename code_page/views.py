from .models import Code_Page
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Code_Page

class PostDetailView(DetailView):
    model = Code_Page