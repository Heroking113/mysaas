# -*- coding: utf-8 -*-

from django.conf.urls import url

from home_application import views

app_name = 'home_application'
urlpatterns = (
    url(r'^$', views.index),
    url(r'^query_all_info/$', views.query_all_info, name='query_all_info'),
    url(r'^query_host_info/$', views.query_host_info, name='query_host_info'),
    url(r'^execute_script/$', views.execute_script, name="execute_script"),
    url(r'^query_record/$', views.query_record, name="query_record"),
    url(r'^retrive_record/$', views.retrive_record, name="retrive_record")
)
