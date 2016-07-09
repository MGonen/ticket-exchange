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

    url(r'tickets/for-sale/$', views.my_tickets_for_sale, name='my_tickets_for_sale'),
    url(r'tickets/bought/$', views.my_tickets_bought, name='my_tickets_bought'),
    # url(r'my-wanted_listings/$', views.my_wanted_listings, name='my_wanted_listings'),
    url(r'payouts/$', views.my_payouts, name='my_payouts'),
    url(r'profile/$', views.my_profile, name='my_profile'),








)
