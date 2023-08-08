from django.urls import path, include
from .views import *
from . views_accounts import *
from .views_counselor import *

urlpatterns = [
    path('login/', AdminLogin.as_view()),
    path('add-counselor/', CounselorRegistration.as_view()),
    path('verify-counselor/<token>', CounselorEmailValidation.as_view(),
         name='verify-counselor-token'),

    path('list-users/', ListUsers.as_view()),
    path('manage-user/<int:pk>/', ManageUser.as_view()),

    path('add-services/', AddServices.as_view()),
    path('list-services/', ListServices.as_view()),
    path('manage-service/<int:pk>/', ManageServices.as_view()),
    path('update-service/<int:pk>/', UpdateServices.as_view()),
    path('delete-service/<int:pk>/', DeleteServices.as_view()),
    path('list-psychological-tasks/', ListPsychologicalTasks.as_view()),
    path('add-psychological-tasks/', AddPsychologicalTasks.as_view()),
    path('add-task-items/<int:id>/', AddTaskItems.as_view()),
    path('update-psychological-tasks/<int:id>/', UpdatePsychologicalTasks.as_view()),
    path('delete-psychological-tasks/<int:id>/', DeletePsychologicalTasks.as_view()),
    path('update-task-items/<int:id>/', UpdateTaskItems.as_view()),
    path('delete-task-items/<int:id>/', DeleteTaskItems.as_view()),
    path('manage-psychological-task/<int:id>/', ManagePsychologialTask.as_view()),

    path('list-counselors/', ListCounselors.as_view()),
    path('manage-counselor/<int:pk>/', ManageCounselor.as_view()),
    path('list-education-request/', ListEducationRequests.as_view()),
    path('list-experience-request/', ListExperienceRequests.as_view()),
    path('get-education-details/<int:id>/', GetEducationDetails.as_view()),
    path('get-experience-details/<int:id>/', GetExperienceDetails.as_view()),
    path('verify-education-request/<int:id>/', verify_education_requests),
    path('verify-experience-request/<int:id>/', verify_experience_requests),
    path('decline-education-request/<int:id>/', DeclineEducationRequest.as_view()),
    path('decline-experience-request/<int:id>/', DeclineExperienceRequest.as_view()),
]
