"""us_election dashboard URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^map$', views.map_view, name="map"),
    url(r'^ajax_map$', views.map_data_ajax, name="ajax_map"),
]
