from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/',CounselorLogin.as_view()),
    path('change-password/<int:id>/',ChangePassword.as_view()),
    path('counselor-profile/<int:id>/', CounselorProfile.as_view()),
    path('add-education/', AddCounselorEducation.as_view()),
    path('get-education/<int:id>/', get_educational_details, name='get-education'),
    path('add-experience/', AddCounselorExperience.as_view()),
    path('get-experience/<int:id>/', get_experience_details),
    path('update-profile-image/<int:id>/', UpdateCounselorProfilePicture.as_view()),
    path('remove-profile-image/<int:id>/', DeleteCounselorProfilePicture.as_view()),
    path('update-profile/<int:id>/', UpdateCounselorProfile.as_view()),
    path('get-counselor-account/<int:id>/', GetCounselorAccount.as_view()),
    path('add-counselor-account/<int:id>/', UpdateCounselorAccounts.as_view()),
    path('update-counselor-account/<int:id>/', UpdateCounselorAccounts.as_view()),
    path('list-services/', ListSpecializations.as_view()),
] 
