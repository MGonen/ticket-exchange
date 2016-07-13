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
from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = (
    url(r'^$', views.home, name='home'),

    url(r'^get_search_results/(?P<search_query>.+)/$', views.get_ajax_search_results, name='get_ajax_search_results'),
    url(r'^advanced_search/(?P<search_query>.+)/$', views.advanced_search, name='advanced_search'),

    url(r'^create_event/$', views.create_event, name='create_event'),
    url(r'^event/(?P<event_pk>[0-9]+)/tickets/$', views.event_tickets, name='event_tickets'),

    url(r'^buy-ticket/(?P<ticket_id>[0-9]+)/$', views.buy_ticket, name='buy_ticket'),

    url(r'^facebook-login-handler/$', views.facebook_login_handler, name='facebook_login_handler'),

    url(r'^fb_logout/$', views.fb_logout, name='fb_logout'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

)
