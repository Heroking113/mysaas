# -*- coding: utf-8 -*-

from django.conf.urls import url

from home_application import views

app_name = 'home_application'
urlpatterns = (
    url(r'^$', views.index),
    url(r'^execute-mission/$', views.execute_mission, name='execute_mission'),
    url(r'^mission-record/$', views.mission_record, name='mission_record'),
    url(r'^query-host-info/$', views.query_host_info, name='query_host_info'),
    url(r'^execute-script/$', views.execute_script, name="execute_script"),
    url(r'^query-record/$', views.query_record, name="query_record"),
    url(r'^user/$', views.get_user, name="get_user")
)
