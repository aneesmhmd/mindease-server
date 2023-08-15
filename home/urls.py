from django.urls import path
from .views import *

urlpatterns = [
    path('services-list/',GetServicesList.as_view()),
    path('counselors-list/',ListCounselors.as_view()),
    path('list-psychological-tasks/',ListPsychologicalTasks.as_view()),
    path('get-psychological-task/<int:id>/',GetPsychologicalTaskDetails.as_view()),
    path('task-subscription-checkout-session/',SubscriptionCheckoutSession.as_view()),
    path('create-task-subscription/',CreateTaskSubscription.as_view()),
    path('get-counselor-profile/<int:id>/',GetCounselorProfile.as_view()),
    path('get-counselor-education/<int:id>/',GetCounselorEducations.as_view()),
    path('get-counselor-experience/<int:id>/',GetCounselorExperience.as_view()),
    path('add-callback-reqs/',AddCallBackReqs.as_view()),
]
