from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from counselor.models import CounselorProfile
from .models import Account
from .serializers import UserRegisterSerializer, GoogleAuthSerializer, MyTokenObtainPairSerializer
from .token import create_jwt_pair_tokens

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate


from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/token/',
        '/token/refresh',
    ]
    return Response(routes)


class UserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password =request.data.get('password')

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.set_password(password)
            user.save()

            if user.is_staff:
                user.role = 'counselor'
                CounselorProfile.objects.create(counselor=user)

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('user/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'cite' : current_site
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'A verificaiton link sent to your registered email address', "data": serializer.data})
        else:
            print('Serializer errors are :',serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


@api_view(['GET'])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        message = 'Congrats! Account activated!'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message
    else:
        message = 'Invalid activation link'
        redirect_url = 'http://localhost:5173/login/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GoogleAuthentication(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if not Account.objects.filter(email=email).exists():
            serializer = GoogleAuthSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.is_active = True
                user.set_password(password)
                user.save()

        user = authenticate(request, email=email, password=password)
        if user is not None:

            tokens = create_jwt_pair_tokens(user)
            response = {
                'msg': "Login successfull",
                'token': tokens,
                'status': 200
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={'msg': 'Login Failed', 'status': 400})


class ForgotPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('user/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({'status': 'success', 'msg': 'Please reset password by verifying the link', 'user_id': user.id})
        else:
            return Response({'status': 'error', 'msg': 'No account registered with this email'})


@api_view(['GET'])
def reset_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
       
        return HttpResponseRedirect(f'http://localhost:5173/reset-password/')


class ResetPassword(APIView):
    def post(self, request, format=None):
        str_user_id = request.data.get('user_id')
        uid = int(str_user_id)
        password = request.data.get('password')

        if uid:
            user = Account.objects.get(id=uid)
            user.set_password(password)
            user.save()

            return Response({'msg': 'Password reset succesfully'})

        return HttpResponseRedirect('http://localhost:5173/login/')

class UpdateUserProfile(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserRegisterSerializer