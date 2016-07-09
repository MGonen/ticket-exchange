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

    url(r'my-tickets/for-sale/$', views.my_tickets_for_sale, name='my_tickets_for_sale'),
    url(r'my-tickets/bought/$', views.my_tickets_bought, name='my_tickets_bought'),
    # url(r'my-wanted_listings/$', views.my_wanted_listings, name='my_wanted_listings'),
    url(r'my-payouts/$', views.my_payouts, name='my_payouts'),
    url(r'my-profile/$', views.my_profile, name='my_profile'),

    url(r'sell-ticket', views.sell_ticket, name='sell_ticket'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),


    # url(r'^person/index/$', views.person_index, name='person_index'),
    # url(r'^person/(?P<person_pk>[0-9]+)/$', views.person_detail, name='person_detail'),
    # url(r'^person/(?P<person_pk>[0-9]+)/edit/$', views.person_edit, name='person_edit'),
    #
    url(r'^event/index/$', views.event_index, name='event_index'),
    # url(r'^event/new/$', views.event_new, name='event_new'),
    # url(r'^event/(?P<event_pk>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^event/(?P<event_pk>[0-9]+)/edit/$', views.event_edit, name='event_edit'),
    #
    #
    # url(r'^ticket/index/$', views.ticket_index, name='ticket_index'),
    # url(r'^ticket/new/$', views.ticket_new, name='ticket_new'),
    # url(r'^ticket/(?P<ticket_pk>[0-9]+)/$', views.ticket_detail, name='ticket_detail'),
    # url(r'^ticket/(?P<ticket_pk>[0-9]+)/edit/$', views.ticket_edit, name='ticket_edit'),
    #
    # url(r'^admin_home/$', views.admin_home, name='admin_home'),



)
