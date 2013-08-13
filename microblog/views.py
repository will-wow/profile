from django.views.generic import TemplateView

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