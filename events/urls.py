from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = (
    url(r'^create/$', views.CreateEvent.as_view(), name='create_event'),
    url(r'^(?P<event_id>[0-9]+)/edit/$', views.EditEvent.as_view(), name='edit_event'),
    url(r'^create-test-baseticket/$', views.create_test_baseticket, name='create_test_baseticket'),
)