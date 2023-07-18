from django.urls import path, include
from . views import *

urlpatterns = [
    path('add-counselor/', CounselorRegistration.as_view()),
    path('verify-counselor/<token>',CounselorEmailValidation.as_view(), name='verify-counselor-token')
   
]
