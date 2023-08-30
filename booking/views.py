from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.conf import settings
from decouple import config

from .models import *
from .serializers import *
from counselor.models import CounselorAccount
from accounts.models import Account

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


class ListAvailableSlots(APIView):
    def post(self, request, id):
        date = request.data.get('selectedDate')
        slots = TimeSlots.objects.filter(
            counselor__id=id, date=date, is_booked=False)
        if slots.exists():
            serializer = TimeSlotSerializer(slots, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={'message': 'No available slots on the selected date!'},
            status=status.HTTP_404_NOT_FOUND
        )


class BookingCheckoutSession(APIView):
    def post(self, request):
        data = request.data
        user_id = data['user']
        counselor_id = data['counselor']
        amount = int(data['amount'])
        date = data['date']
        slot_id = data['slot']

        try:
            user = Account.objects.get(id=user_id, is_active=True)
        except Account.DoesNotExist:
            return Response(
                data={'message': "Invalid user"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            counselor = CounselorAccount.objects.get(
                id=counselor_id, is_verified=True)
        except CounselorAccount.DoesNotExist:
            return Response(
                data={'message': 'The selected counselor not found!'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            slot = TimeSlots.objects.get(id=slot_id, is_booked=False)
        except TimeSlots.DoesNotExist:
            return Response(
                data={'message': 'Invalid slot'},
                status=status.HTTP_404_NOT_FOUND
            )

        appointment = Appointments.objects.create(
            user=user, counselor=counselor, slot=slot, session_date=date)
        slot.is_booked = True
        slot.save()

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': 'Counselor Slot Booking'
                        },
                        'unit_amount': amount * 100
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=config('booking_success_url') +
                '?appointment=' + str(appointment.id),
                cancel_url=config('booking_cancel_url')
            )
            return Response(data=checkout_session.url, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(data={'message': 'Oops!Some error occured'})


class AppointmentPaymentSuccess(APIView):
    def patch(self, request, id):
        try:
            appointment = Appointments.objects.get(id=id, is_paid=False)
            appointment.is_paid = True
            appointment.amount_paid = appointment.counselor.fee
            appointment.save()
            return Response(status=status.HTTP_200_OK)
        except Appointments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ListAppointments(APIView):
    def get(self, request, id):
        appointments = Appointments.objects.filter(user__id=id, is_paid=True)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetRoomLink(APIView):
    def get(self, request, id):
        try:
            link = MeetLink.objects.get(user__id=id)
            serializer = MeetLinkSerializer(link, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except MeetLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class GetAppointmentDetails(generics.RetrieveAPIView):
    queryset = Appointments.objects.filter(is_rescheduled=False)
    serializer_class = AppointmentSerializer


class RescheduleSession(APIView):
    def patch(self, request, id):
        rescheduled_date = request.data.get('date')
        rescheduled_slot = request.data.get('slot')
        slot = TimeSlots.objects.get(id=rescheduled_slot)
        try:
            appointment = Appointments.objects.get(
                id=id, status='Not attended')

            if appointment.is_rescheduled:
                return Response(
                    data={'message': 'Session rescheduled!'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            appointment.slot = slot
            appointment.session_date = rescheduled_date
            appointment.status = 'Pending'
            appointment.is_rescheduled = True
            appointment.save()
            return Response(
                data={'message': 'Session rescheduled succesfully'},
                status=status.HTTP_200_OK
            )

        except Appointments.DoesNotExist:
            return Response(
                data={'message': 'No valid session found'},
                status=status.HTTP_404_NOT_FOUND
            )
