#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ChukovNA'

from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
)
