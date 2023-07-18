from counselor.models import CounselorProfile
from accounts.serializers import UserRegisterSerializer
from .helpers import generate_token
from .models import RandomTokenGenerator

from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from decouple import config

# Create your views here.

class CounselorRegistration(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data['values'])
        print('Its reached here', serializer)
        if serializer.is_valid(raise_exception=True):
           

            user = serializer.save()
            user.is_staff, user.role = True, 'counselor'
            user.save()
            CounselorProfile.objects.create(counselor=user)

            activation_token = generate_token(id=user.id)
            activation_url = self.request.build_absolute_uri(
                reverse('verify-counselor-token', kwargs={'token': activation_token}))

            mail_subject = 'Activate your account'
            message = render_to_string('accounts/counselor_activation.html', {
                'user': user,
                'activation_url': activation_url
            })

            result = send_mail(mail_subject, message,
                               settings.EMAIL_HOST_USER, [user.email])
            if result:
                RandomTokenGenerator.objects.create(token=activation_token, user=user)

            return Response({'msg': 'Counselor added succesfully!', 'status': 200})
        return Response({'msg': 'Oops! Registration failed'})


class CounselorEmailValidation(APIView):
    def get(self, request, token):
        redirect_url = config('BaseUrl')
        try:
            validated = RandomTokenGenerator.objects.get(token=token)
            print('validate token is :', validated.user.first_name)
            validated.user.is_active = True
            validated.user.save()
            validated.delete()
            message = 'Account Activated,please set password'
            return HttpResponseRedirect(redirect_url + 'counselor/set-password/?message=' + message)
        
        except RandomTokenGenerator.DoesNotExist:
            message = 'Invalid token'
            return HttpResponseRedirect(redirect_url + 'login/?message=' + message)
