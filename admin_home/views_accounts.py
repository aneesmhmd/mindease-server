from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from counselor.models import CounselorAccount
from accounts.serializers import UserRegisterSerializer, ProfilePictureUpdateSerializer
from .serializers import UserSerializer
from accounts.models import Account
from .helpers import generate_token, generate_random_password
from .models import RandomTokenGenerator
from accounts.token import create_jwt_pair_tokens

from decouple import config

# Create your views here.


class AdminLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        print(f'User is {user}')

        if user is not None:
            if user.is_active and user.is_admin and user.role == 'admin':
                tokens = create_jwt_pair_tokens(user)
                response = {
                    'message': 'Login succesfull',
                    'token': tokens
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Unauthorized access'}
                return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)
        else:

            response = {'message': 'Invalid login credentials'}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class CounselorRegistration(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        password = request.data.get('password')
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.is_staff, user.role = True, 'counselor'
            user.save()
            CounselorAccount.objects.create(counselor=user)
            print('User is :', user, ' with password ', password)

            activation_token = generate_token()
            print('This is our token:', activation_token)
            activation_url = self.request.build_absolute_uri(
                reverse('verify-counselor-token', kwargs={'token': activation_token}))

            mail_subject = 'Activate your account'
            message = render_to_string('counselor/counselor_activation.html', {
                'user': user,
                'activation_url': activation_url
            })

            result = send_mail(mail_subject, message,
                               settings.EMAIL_HOST_USER, [user.email])
            print(result)
            if result:
                RandomTokenGenerator.objects.create(
                    token=activation_token, user=user)

                return Response({'msg': 'Counselor added succesfully!', 'status': 200})
        return Response({'msg': 'Oops! Registration failed'})


class CounselorEmailValidation(APIView):
    def get(self, request, token):
        redirect_url = config('BaseUrl')
        try:
            validated = RandomTokenGenerator.objects.get(
                token=token)

            '''
            If the validation coupon exists, a random password is generated 
            and will be sent to the verified email. And deletes the token.
            '''
            password = generate_random_password()
            mail_subject = 'Account Verified'
            message = render_to_string('counselor/password_mail.html', {
                'user': validated.user,
                'password': password
            })

            print('No error till here')

            result = send_mail(mail_subject, message,
                               settings.EMAIL_HOST_USER, [validated.user.email])
            print('This reached here also')

            if result:
                validated.user.is_active = True
                validated.user.set_password(password)
                validated.user.save()

            validated.delete()
            return HttpResponseRedirect(redirect_url + 'counselor/login/?message=Congrats!Check your email.')

        except RandomTokenGenerator.DoesNotExist:
            message = 'Invalid token'
            return HttpResponseRedirect(redirect_url + 'login/?message=' + message)


class ListUsers(ListAPIView):
    queryset = Account.objects.filter(role='user').order_by('-id')
    serializer_class = UserSerializer


class ManageUser(APIView):
    def patch(self, request, pk):
        try:
            user = Account.objects.get(id=pk, role='user')
            user.is_active = not user.is_active
            user.save()
            if user.is_active:
                message = 'User Unblocked'
            else:
                message = 'User blocked'
            return Response(data={'message': message}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(data={'message': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)


class GetAdminProfile(RetrieveAPIView):
    queryset = Account.objects.filter(role='admin', is_admin=True)
    serializer_class = UserSerializer
    lookup_field = 'id'


class UpdateAdminProfile(UpdateAPIView):
    queryset = Account.objects.filter(role='admin')
    serializer_class = UserSerializer
    lookup_field = 'id'


class UpdateAdminProfilePicture(UpdateAPIView):
    queryset = Account.objects.filter(role='admin')
    serializer_class = ProfilePictureUpdateSerializer
    lookup_field = 'id'


class ChangeAdminPassword(APIView):
    def post(self, request, id):
        try:
            user = Account.objects.get(id=id, role='admin')
        except Account.DoesNotExist:
            return Response(
                data={'message': 'No active account'},
                status=status.HTTP_404_NOT_FOUND
            )

        current_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(
                data={'message': 'Password reset succesfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )