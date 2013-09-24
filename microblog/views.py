from django.views.generic import TemplateView
from django.shortcuts import render

class HomepageView(TemplateView):
    template_name = 'index.html'

def sitePassView(request, *args, **kwargs):
    template_name = "sitePass.html"
    return render(request, template_name)