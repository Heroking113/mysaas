# -*- coding: utf-8 -*-

from django.conf.urls import url

from home_application import views

app_name = 'home_application'
urlpatterns = (
    url(r'^$', views.index),
    url(r'^query_all_info/$', views.query_all_info, name='query_all_info'),
    url(r'^mission-record/$', views.mission_record, name='mission_record'),
    url(r'^query_host_info/$', views.query_host_info, name='query_host_info'),
    url(r'^execute_script/$', views.execute_script, name="execute_script"),
    url(r'^query-record/$', views.query_record, name="query_record")
)
