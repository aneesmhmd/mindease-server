from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import status
from rest_framework.validators import ValidationError
from datetime import datetime, timedelta

from . models import *
from . serializers import *
from booking.models import TimeSlots
from booking.serializers import TimeSlotSerializer
from counselor.serializers import (
    CounselorAccountSerializer,
    CounselorAccount,
    CounselorEducation,
    CounselorEducationSerializer,
    CounselorExperience,
    CounselorExperienceSerializer,
)
from admin_home.serializers import (
    PsychologicalTaskSerializer,
    PsychologicalTasks,
    ServicesSerializer,
    CallBackReqsSerializer,
    TaskSubscriptionSerialzer,
)

from django.conf import settings
from decouple import config

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class GetServicesList(APIView):
    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)


class ListCounselors(ListAPIView):
    queryset = CounselorAccount.objects.filter(is_verified=True)
    serializer_class = CounselorAccountSerializer


class GetCounselorProfile(RetrieveAPIView):
    queryset = CounselorAccount.objects.filter(is_verified=True)
    serializer_class = CounselorAccountSerializer
    lookup_field = 'id'


class GetCounselorEducations(APIView):
    def get(self, request, id):
        educations = CounselorEducation.objects.filter(
            counselor__id=id, is_verified=True)
        serializer = CounselorEducationSerializer(educations, many=True)
        return Response(data=serializer.data)


class GetCounselorExperience(APIView):
    def get(self, request, id):
        experiences = CounselorExperience.objects.filter(
            counselor__id=id, is_verified=True)
        serializer = CounselorExperienceSerializer(experiences, many=True)
        return Response(data=serializer.data)


class ListPsychologicalTasks(ListAPIView):
    queryset = PsychologicalTasks.objects.filter(is_active=True)
    serializer_class = PsychologicalTaskSerializer


class GetPsychologicalTaskDetails(RetrieveAPIView):
    queryset = PsychologicalTasks.objects.filter(is_active=True)
    serializer_class = PsychologicalTaskSerializer
    lookup_field = 'id'


class GetPsychologistDetails(RetrieveAPIView):
    queryset = CounselorAccount.objects.filter(is_verified=True)
    serializer_class = CounselorAccountSerializer
    lookup_field = 'id'


class SubscriptionCheckoutSession(APIView):
    def post(self, request):
        data = request.data
        title = data['title']
        price = int(data['amount']) * 100
        image = [data['image']]
        task_id = data['taskId']
        task = PsychologicalTasks.objects.get(id=task_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': title,
                            'images': image
                        },
                        'unit_amount': price,
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=config('task_success_url')+'?task=' + str(task_id) + '&amount_paid=' + str(
                    data['amount']) + '&validity=' + str(task.validity),
                cancel_url=config('task_cancel_url')
            )
            return Response(data=checkout_session.url)
        except Exception as e:
            print(e)
            return Response(
                data={'message': 'Oops!Some error occured!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateTaskSubscription(CreateAPIView):
    queryset = TaskSubscription.objects.all()
    serializer_class = CreateTaskSubscriptionSerializer

    def perform_create(self, serializer):
        task = self.request.data.get('task')
        user = self.request.data.get('user')
        try:
            TaskSubscription.objects.get(task__id=task, user__id=user)
            raise ValidationError('Already subscribed')
        except TaskSubscription.DoesNotExist:
            days_to_add = serializer.validated_data.get('validity')
            expiry_date = datetime.now().date() + timedelta(days_to_add)
            serializer.save(is_paid=True, expiry_date=expiry_date)
            return super().perform_create(serializer)


class ListSubscribedTasks(APIView):

    def get(self, request, user_id):
        subscribed = TaskSubscription.objects.filter(user__id=user_id)
        serializer = TaskSubscriptionSerialzer(subscribed, many=True)
        return Response(data=serializer.data)


class ListSubscribedTaskItems(APIView):

    def get(self, request, user_id, sub_id):
        try:
            subscribed = TaskSubscription.objects.get(
                id=sub_id, user__id=user_id, is_expired=False)
            task = subscribed.task
            task_items = TaskItems.objects.filter(task=task)
            serializer = RetrieveTaskItemsSerializer(task_items, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except TaskSubscription.DoesNotExist:
            return ValidationError('No active subscription found')


class AddCallBackReqs(CreateAPIView):
    queryset = CallBackReqs.objects.all()
    serializer_class = CallBackReqsSerializer
