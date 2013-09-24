from .models import Section, Slice, Grid
from django.views.generic import DetailView, ListView

class SectionView(DetailView):
    model = Section
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SectionView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the sections
        context['slice_list'] = Slice.objects.filter(section=context['section'].id)
        context['grid_list'] = []
        # filter the grids and add them
        for slice in context['slice_list']:
            slice.type = (slice.sort_key + 1) % 2
            context['grid_list'] += Grid.objects.filter(slice=slice.id)
        # header
        context['nav_list'] = Section.objects.exclude(slug='footer')
        # footer
        footer_section = Section.objects.filter(slug='footer')
        context['footer_slice'] = Slice.objects.filter(section=footer_section[0].id)[0]
        context['footer_grid_list'] = Grid.objects.filter(slice=context['footer_slice'].id)
        
        return context

class HomeView(ListView):
    model = Section
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['nav_list'] = Section.objects.exclude(slug='footer').order_by('sort_key')
        # footer
        footer_section = Section.objects.filter(slug='footer')
        context['footer_slice'] = Slice.objects.filter(section=footer_section[0].id)[0]
        context['footer_grid_list'] = Grid.objects.filter(slice=context['footer_slice'].id)
        
        return context