from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
)
