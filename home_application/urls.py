# -*- coding: utf-8 -*-

from django.conf.urls import url

from home_application import views

app_name = 'home_application'
urlpatterns = (
    url(r'^$', views.index),
    url(r'^dev-guide/$', views.dev_guide),
    url(r'^contact/$', views.contact),
    url(r'^helloworld/$', views.helloworld),
    url(r'^execute-mission/$', views.execute_mission, name='execute_mission'),
    url(r'^mission-record/$', views.mission_record, name='mission_record'),
    url(r'^get-host-info/$', views.get_host_info, name='get_host_info')
)
