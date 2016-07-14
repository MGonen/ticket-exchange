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

    url(r'^ticket-details/(?P<ticket_id>[0-9]+)/$', views.ticket_details, name='ticket_details'),
    url(r'^personal-details/(?P<ticket_id>[0-9]+)/$', views.confirm_personal_details, name='confirm_personal_details'),
    url(r'^payment-method/(?P<ticket_id>[0-9]+)/$', views.select_payment_method, name='select_payment_method'),
    url(r'^payment-confirmation/(?P<ticket_id>[0-9]+)/$', views.payment_confirmation, name='payment_confirmation'),
    url(r'^payment-failed/(?P<ticket_id>[0-9]+)/$', views.payment_failed, name='payment_failed'),

)
