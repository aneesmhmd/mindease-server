from django.urls import path
from .views import *

urlpatterns = [
    path('services-list/',GetServicesList.as_view()),
    path('counselors-list/',ListCounselors.as_view()),
    path('list-psychological-tasks/',ListPsychologicalTasks.as_view()),
] 
