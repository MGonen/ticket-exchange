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
    url(r'^select_event/$', views.SelectEvent.as_view(), name='select_event'),

    url(r'^(?P<event_id>[0-9]+)/tickets/$', views.AvailableTickets.as_view(), name='available_tickets'),
    url(r'^(?P<event_id>[0-9]+)/get_available_tickets/$', views.get_available_tickets_ajax, name='get_available_tickets'),
    url(r'^potential_buyer_check/(?P<ticket_id>[0-9]+)/$', views.potential_buyer_check, name='potential_buyer_check'),

    url(r'^purchase/(?P<ticket_id>[0-9]+)/$', views.Purchase.as_view(), name='purchase'),
    url(r'^(?P<ticket_id>[0-9]+)/purchase/time-left/$', views.purchase_time_left, name='purchase_time_left'),

    url(r'^cancel-ticket/(?P<ticket_id>[0-9]+)/$', views.cancel_ticket_view, name='cancel_ticket_view'),
    url(r'^payment/token/$', views.get_braintree_token, name='get_braintree_token'),
    url(r'^personal-info-ajax/$', views.personal_info_ajax, name='personal_info_ajax'),

)
