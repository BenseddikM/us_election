"""us_election dashboard URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="dashboard"),
    url(r'^map$', views.map_view, name="map"),
    url(r'^state$', views.state_view, name="state"),

]
