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

    url(r'tickets/for-sale/$', views.tickets_for_sale, name='tickets_for_sale'),
    url(r'tickets/for-sale/(?P<ticket_id>[0-9]+)/$', views.ticket_for_sale_details, name='ticket_for_sale_details'),
    url(r'tickets/bought/$', views.tickets_bought, name='tickets_bought'),
    url(r'tickets/bought/(?P<ticket_id>[0-9]+)/$', views.ticket_bought_details, name='ticket_bought_details'),
    # url(r'my-wanted_listings/$', views.my_wanted_listings, name='my_wanted_listings'),
    url(r'payouts/$', views.payouts, name='payouts'),
    url(r'profile/$', views.profile, name='profile'),

)
