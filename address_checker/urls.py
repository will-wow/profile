from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$',views.addresses),
    url(r'^split/?$',views.ajax_addresses),
)
