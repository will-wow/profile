from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$',views.HomeView.as_view(), name='front'),
    url(r'^(?P<slug>[\w-]+)/$', views.SectionView.as_view(), name='section'),
)
