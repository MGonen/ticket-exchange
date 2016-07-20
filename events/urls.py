from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = (
    url(r'^create/$', views.create_event, name='create_event'),
    url(r'^(?P<event_id>[0-9]+)/tickets/$', views.event_tickets, name='event_tickets'),
    url(r'^(?P<event_id>[0-9]+)/get_event_tickets/$', views.get_event_tickets, name='get_event_tickets'),
    url(r'^(?P<event_id>[0-9]+)/edit/$', views.edit_event, name='edit_event'),
)