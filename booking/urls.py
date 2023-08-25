from django.urls import path, include
from .views import *

urlpatterns = [
    path('list-available-slots/<int:id>/',ListAvailableSlots.as_view()),
    path('create-checkout-session/',BookingCheckoutSession.as_view()),
    path('payment-success/<int:id>/',AppointmentPaymentSuccess.as_view()),
    path('list-appointments/<int:id>/',ListAppointments.as_view()),
    path('reschedule-session/<int:id>/',RescheduleSession.as_view()),
    path('get-meet-link/<int:id>/',GetMeetLink.as_view()),
]