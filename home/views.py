from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework import status

from . models import *
from counselor.serializers import (
    CounselorAccountSerializer,
    CounselorAccount,
    CounselorEducation,
    CounselorEducationSerializer,
    CounselorExperience,
    CounselorExperienceSerializer
)
from admin_home.serializers import (
    PsychologicalTaskSerializer,
    PsychologicalTasks,
    ServicesSerializer,
    CallBackReqsSerializer,
    TaskSubscriptionSerialzer
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
                success_url=config('success_url')+'?task=' + str(task_id) + '&amount_paid=' + str   (data['amount']),
                cancel_url=config('cancel_url')
            )
            return Response(data=checkout_session.url)
        except Exception as e:
            print(e)
            return Response(data={'message': 'Oops!Some error occured!'}, status=status.HTTP_400_BAD_REQUEST)
        
class CreateTaskSubscription(CreateAPIView):
    queryset = TaskSubscription.objects.all()
    serializer_class = TaskSubscriptionSerialzer

    def perform_create(self, serializer):
        serializer.save(is_paid=True)
        return super().perform_create(serializer)


class AddCallBackReqs(CreateAPIView):
    queryset = CallBackReqs.objects.all()
    serializer_class = CallBackReqsSerializer
