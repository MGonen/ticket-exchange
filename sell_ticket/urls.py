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
    url(r'^selected-event/(?P<event_id>[0-9]+)/$', views.selected_event, name='selected_event'),
    url(r'^upload-ticket/$', views.upload_ticket, name='upload_ticket'),
    url(r'^set-price/$', views.set_price, name='set_price'),
    url(r'^personal-details/$', views.personal_details, name='personal_details'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),







)
