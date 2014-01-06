from django.shortcuts import render
from forms import AddressForm
import SplitAddress
from section.views import add_header_footer
from django.http import HttpResponse
import json

def addresses(request):
    context={}
    context = add_header_footer(context)
    return render(request,'address_checker/splitter.html',context)

def ajax_addresses(request):
    split={}
    
    if request.is_ajax():
        form=AddressForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            sr = SplitAddress.Splitter_Regex()
            split = SplitAddress.Splitter(sr,cd['address1'],cd['address2'],cd['has_attn']).addys
            #return render(request,'address_checker/splitter.html',context)
            return HttpResponse(json.dumps(split), content_type="application/json")