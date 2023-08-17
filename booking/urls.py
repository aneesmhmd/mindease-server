from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-appointment-slot/',CreateSlots.as_view()),
    path('create-checkout-session/',BookingCheckoutSession.as_view()),
]