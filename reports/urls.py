#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ChukovNA'
from django.conf.urls import patterns, url

from reports import views

urlpatterns = patterns('',

                       url(r'$', views.index, name='index'), #this record mast be last!!!!
)