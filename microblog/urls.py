from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'microblog.views.home', name='home'),
    # url(r'^microblog/', include('microblog.foo.urls')),
    url(r'^$', views.HomepageView.as_view(), name='home'),
    
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
    url(r'^blog/', include('blog.urls', namespace='blog')),
    
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^code/', include('code_page.urls', namespace='code_page'), name='code_page'),
    url(r'^design/', views.DesignView.as_view(), name='design'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
    
    url(r'^sitePass/', views.sitePassView, name='sitePass'),
    
    url(r'^admin/', include(admin.site.urls)),
)