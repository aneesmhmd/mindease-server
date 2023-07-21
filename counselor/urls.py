from django.contrib import admin
from django.urls import path
from .views import CounselorLogin

urlpatterns = [
    path('login/',CounselorLogin.as_view()),
] 
