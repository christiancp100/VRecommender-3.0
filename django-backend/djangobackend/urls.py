"""djangobackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from djangoapi.healthcheck import healthcheck
from djangoapi import search
from djangoapi import map

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck', healthcheck, name = "healthcheck"),
    path('describe/', search.describe, name = "describe"),
    path('distribution/', search.distribution, name = "distribution"),
    path('create-chart/', search.createChart, name = "createChart"),
    path('type-of-chart/', search.chartType, name = "chartType"),
    path('columns/',search.allColumnType, name = "coloumns type"),
    path('map/airports/', map.airports, name="airports"),
    path('map/flights/', map.flights, name="flights"),
]
