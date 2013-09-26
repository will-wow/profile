from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitePass', views.sitePassView, name='sitePass'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('section.urls', namespace='section')),
)