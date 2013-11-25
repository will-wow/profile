from django.shortcuts import render
from forms import AddressForm
import SplitAddress
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from section.models import Section, Slice, Grid
from section.views import add_header_footer

def addresses(request):
    context={}
    context = add_header_footer(context)
    
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
