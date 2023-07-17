from django.urls import path, include
from . views import CounselorRegistration

urlpatterns = [
    path('add-counselor/', CounselorRegistration.as_view()),
   
]
