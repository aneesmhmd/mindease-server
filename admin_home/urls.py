from django.urls import path, include
from . views_accounts import *

urlpatterns = [
    path('login/', AdminLogin.as_view()),
    path('add-counselor/', CounselorRegistration.as_view()),
    path('verify-counselor/<token>',CounselorEmailValidation.as_view(), name='verify-counselor-token'),
    
    path('list-users/', ListUsers.as_view()),
    path('list-counselors/', ListCounselors.as_view()),
    path('manage-user/<int:pk>/', ManageUser.as_view()),
    path('manage-counselor/<int:pk>/', ManageCounselor.as_view()),
]
