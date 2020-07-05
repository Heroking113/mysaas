# -*- coding: utf-8 -*-

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from home_application import views

router = DefaultRouter()
router.register(r'records', views.MissionRecordViewSet, basename="mission_records")

app_name = 'home_application'
urlpatterns = [
    path('', views.index),
    path('deliever_log/', views.deliever_log, name="deliever_log"),
    path('query_all_info/', views.query_all_info, name='query_all_info'),
    path('retrieve_host/', views.retrieve_host, name="retrieve_host"),
    path('execute_script/', views.execute_script, name="execute_script"),
    path('query_host_by_business/', views.query_host_by_business, name="query_host_by_business")
]

urlpatterns += [path('', include(router.urls))]
