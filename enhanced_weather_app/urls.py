from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from enhanced_weather_app import views

urlpatterns = [
    path('', views.default_page, name='default_page'),
    path('', views.index, name='index'),
    path('', views.call_api, name='call_api'),
    path("__reload__/", include("django_browser_reload.urls")),
]