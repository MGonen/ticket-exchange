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
    url(r'^select_event/$', views.select_event, name='select_event'),
    url(r'^(?P<event_id>[0-9]+)/tickets/$', views.event_tickets, name='event_tickets'),
    url(r'^(?P<event_id>[0-9]+)/get_event_tickets/$', views.get_event_tickets_ajax, name='get_event_tickets'),
    url(r'^potential_buyer_check/(?P<ticket_id>[0-9]+)/$', views.potential_buyer_check, name='potential_buyer_check'),
    url(r'^ticket-details/(?P<ticket_id>[0-9]+)/$', views.ticket_details, name='ticket_details'),
    url(r'^cancel-ticket/(?P<ticket_id>[0-9]+)/$', views.cancel_ticket_view, name='cancel_ticket_view'),
    url(r'^personal-details/(?P<ticket_id>[0-9]+)/$', views.confirm_personal_details, name='confirm_personal_details'),
    url(r'^payment-method/(?P<ticket_id>[0-9]+)/$', views.select_payment_method, name='select_payment_method'),
    url(r'^confirm-purchase/(?P<ticket_id>[0-9]+)/$', views.confirm_purchase, name='confirm_purchase'),
    url(r'^payment-confirmation/(?P<ticket_id>[0-9]+)/$', views.payment_confirmation, name='payment_confirmation'),
    url(r'^payment-failed/(?P<ticket_id>[0-9]+)/$', views.payment_failed, name='payment_failed'),

)
