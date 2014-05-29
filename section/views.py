from .models import Section, Slice, Grid, Link
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from forms import ContactEmail
from django.views.decorators.csrf import csrf_exempt
from settings import CONTACT_EMAIL_TO
import json, smtplib

def add_header_footer(context):
    '''add the header and footer to the context'''
    # header
    context['nav_list'] = Section.objects.exclude(slug='footer').order_by('sort_key').filter(nav=True)
    print('nav list:')
    print(context['nav_list'])
    # footer
    footer_section = Section.objects.filter(slug='footer')
    context['footer_slice'] = Slice.objects.filter(section=footer_section[0].id)[0]
    context['footer_grid_list'] = Grid.objects.filter(slice=context['footer_slice'].id)
    context['footer_link_list']=[]
    for grid in context['footer_grid_list']:
        grid_links = Link.objects.filter(grid=grid.id)
        context['footer_link_list'] += grid_links
    
    return context

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
        
        context = add_header_footer(context)
        
        return context


class HomeView(ListView):
    model = Section
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context = add_header_footer(context)
        
        return context


@csrf_exempt
def contact_view(request):
  if request.is_ajax():
    form=ContactEmail(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      
      try:
        send_mail('Contact Me Email',cd['email'],cd['emailfrom'],[CONTACT_EMAIL_TO],fail_silently=False)
      except Exception as e:
        response = json.dumps({'sent':False,'message':'There was a server error: {}'.format(e)})
      else:
        response = json.dumps({'sent':True,'message':''})
      
      return HttpResponse(response, content_type="application/json")