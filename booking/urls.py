from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-checkout-session/',BookingCheckoutSession.as_view()),
]