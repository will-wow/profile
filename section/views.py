from .models import Section, Slice, Grid, Link
from django.views.generic import DetailView, ListView

def get_max(grid_list):
    max = 0
    max_id = 0
    for grid in grid_list:
        if grid.sort_key > max:
            max = grid.sort_key
            max_id = grid.id
    return max_id

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
            # set the type
            slice.type = (slice.sort_key + 1) % 2
            # get the grids
            slice_grids = Grid.objects.filter(slice=slice.id)
            slice.max = get_max(slice_grids)
            context['grid_list'] += slice_grids
            # links
            context['link_list']=[]
            for grid in context['grid_list']:
                grid_links = Link.objects.filter(grid=grid.id)
                context['link_list'] += grid_links
        
        # header
        context['nav_list'] = Section.objects.exclude(slug='footer').filter(nav=True)
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