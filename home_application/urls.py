# -*- coding: utf-8 -*-

from django.conf.urls import url

from home_application import views

app_name = 'home_application'
urlpatterns = (
    url(r'^$', views.index),
    url(r'^execute-mission/$', views.execute_mission, name='execute_mission'),
    url(r'^mission-record/$', views.mission_record, name='mission_record'),
    url(r'^query-host-info/$', views.query_host_info, name='query_host_info'),
    url(r'^query-specific-host/$', views.query_specific_host, name="query_specific_host")
)
