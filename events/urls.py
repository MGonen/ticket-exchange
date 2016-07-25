from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = (
    url(r'^create/$', views.create_event, name='create_event'),

    url(r'^(?P<event_id>[0-9]+)/edit/$', views.edit_event, name='edit_event'),
)