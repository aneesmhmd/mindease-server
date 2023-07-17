from django.contrib import admin
from django.urls import path
from .views import GetServicesList

urlpatterns = [
    path('services-list/',GetServicesList.as_view()),
] 
