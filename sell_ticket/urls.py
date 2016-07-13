"""TS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

import views

urlpatterns = (

    url(r'^select-event/$', views.select_event, name='select_event'),
    url(r'^incomplete-ticket-check/(?P<event_id>[0-9]+)/$', views.incomplete_ticket_check, name='incomplete_ticket_check'),
    url(r'^event_selected/(?P<ticket_id>[0-9]+)/$', views.event_selected, name='event_selected'),
    url(r'^upload-pdf/(?P<ticket_id>[0-9]+)/$', views.upload_pdf, name='upload_pdf'),
    url(r'^set-price/(?P<ticket_id>[0-9]+)/$', views.set_price, name='set_price'),
    url(r'^personal-details/(?P<ticket_id>[0-9]+)/$', views.personal_details, name='personal_details'),
    url(r'^complete/(?P<ticket_id>[0-9]+)/$', views.completion, name='completion'),

)
