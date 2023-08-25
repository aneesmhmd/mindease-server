from django.urls import path, include
from .views import *
from . views_accounts import *
from .views_counselor import *

urlpatterns = [

    # views_accounts
    path('login/', AdminLogin.as_view()),
    path('is-admin-auth/<int:id>/', IsAdminAuth.as_view()),
    path('add-counselor/', CounselorRegistration.as_view()),
    path('verify-counselor/<token>', CounselorEmailValidation.as_view(),
         name='verify-counselor-token'),
    path('get-admin-profile/<int:id>/', GetAdminProfile.as_view()),
    path('update-profile/<int:id>/', UpdateAdminProfile.as_view()),
    path('update-profile-picture/<int:id>/',
         UpdateAdminProfilePicture.as_view()),
    path('change-password/<int:id>/', ChangeAdminPassword.as_view()),
    path('list-users/', ListUsers.as_view()),
    path('manage-user/<int:pk>/', ManageUser.as_view()),

    # views
    path('dashboard-view/',DashboardView.as_view()),
    path('add-services/', AddServices.as_view()),
    path('list-services/', ListServices.as_view()),
    path('manage-service/<int:pk>/', ManageServices.as_view()),
    path('update-service/<int:pk>/', UpdateServices.as_view()),
    path('delete-service/<int:pk>/', DeleteServices.as_view()),
    path('list-psychological-tasks/', ListPsychologicalTasks.as_view()),
    path('get-psychological-task/<int:id>/',
         GetPyshcologicalTaskDetails.as_view()),
    path('get-task-items/<int:id>/', ListTaskItems.as_view()),
    path('add-psychological-tasks/', AddPsychologicalTasks.as_view()),
    path('add-task-items/<int:id>/', AddTaskItems.as_view(), name='add-task-items'),
    path('update-psychological-tasks/<int:id>/',
         UpdatePsychologicalTasks.as_view()),
    path('update-task-items/<int:id>/', UpdateTaskItems.as_view()),
    path('delete-psychological-tasks/<int:id>/',
         DeletePsychologicalTasks.as_view()),
    path('delete-task-items/<int:id>/', DeleteTaskItems.as_view()),
    path('manage-psychological-task/<int:id>/',
         ManagePsychologialTask.as_view()),
    path('list-task-subscriptions/', ListTaskSubscriptions.as_view()),
    path('list-callback-reqs/', ListCallBackReqs.as_view()),
    path('update-callback-reqs/<int:pk>/', UpdateCallBackReqs.as_view()),
    path('list-all-appointments/', ListAllAppointments.as_view()),

    # views_counselor
    path('list-counselors/', ListCounselors.as_view()),
    path('manage-counselor/<int:pk>/', ManageCounselor.as_view()),
    path('list-education-request/', ListEducationRequests.as_view()),
    path('list-experience-request/', ListExperienceRequests.as_view()),
    path('get-education-details/<int:id>/', GetEducationDetails.as_view()),
    path('get-experience-details/<int:id>/', GetExperienceDetails.as_view()),
    path('verify-education-request/<int:id>/', verify_education_requests),
    path('verify-experience-request/<int:id>/', verify_experience_requests),
    path('decline-education-request/<int:id>/',
         DeclineEducationRequest.as_view()),
    path('decline-experience-request/<int:id>/',
         DeclineExperienceRequest.as_view()),
]
