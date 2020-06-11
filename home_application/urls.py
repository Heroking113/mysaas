# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from home_application import views

# router = DefaultRouter()
# router.register(r'hosts', views.RetrieveHostInfoViewSet, basename="retrieve_hosts")

app_name = 'home_application'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^query_all_info/$', views.query_all_info, name='query_all_info'),
    url(r'^retrieve_host/$', views.retrieve_host, name="retrieve_host")
    # url(r'^query_host_info/$', views.query_host_info, name='query_host_info'),
    # url(r'^execute_script/$', views.execute_script, name="execute_script")
]

# urlpatterns += [path('', include(router.urls))]
