from django.views.generic import TemplateView
from django.shortcuts import render

class HomepageView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class CodeView(TemplateView):
    template_name = 'code.html'

class DesignView(TemplateView):
    template_name = 'design.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

def sitePassView(request, *args, **kwargs):
    template_name = "sitePass.html"
    return render(request, template_name)