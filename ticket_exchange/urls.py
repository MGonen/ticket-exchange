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

    url(r'^facebook-post-login-handler/$', views.facebook_post_login_handler, name='facebook_post_login_handler'),
    url(r'^fb_logout/$', views.fb_logout, name='fb_logout'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

)
