from django.shortcuts import render
from forms import AddressForm
import SplitAddress
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from section.models import Section, Slice, Grid

def addresses(request):
    context={}
    context['nav_list'] = Section.objects.exclude(slug='footer').order_by('sort_key')
    # footer
    footer_section = Section.objects.filter(slug='footer')
    context['footer_slice'] = Slice.objects.filter(section=footer_section[0].id)[0]
    context['footer_grid_list'] = Grid.objects.filter(slice=context['footer_slice'].id)
    
    
    if request.method == 'POST':
        context['form']=AddressForm(request.POST)
        if context['form'].is_valid():
            cd = context['form'].cleaned_data
            sr = SplitAddress.Splitter_Regex()
            context['split'] = SplitAddress.Splitter(sr,cd['address1'],cd['address2'],cd['has_attn']).addys
            return render(request,'address_checker/splitter.html',context)
    else:
        context['form']=AddressForm()
    return render(request,'address_checker/splitter.html',context)
