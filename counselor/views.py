from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CounselorSerializer
from accounts.models import Account
from .models import CounselorProfile
from accounts.token import create_jwt_pair_tokens

# Create your views here.

class CounselorLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        print(f'user is : {user}')
        if user is not None:
            if user.is_active and user.is_staff and user.role=='counselor':
                print('authenticated')
                tokens = create_jwt_pair_tokens(user)
                response = {
                    'message' : 'Login succesfull',
                    'token' : 'token',
                    'status' : 200
                }

                return Response(data=response,status=status.HTTP_200_OK)
            else:
                response = {
                    'message' : 'Unauthorized login',
                    'status' : 401
                }
                return Response(data=response)
        else:
            response = {
                'message' : 'Invalide login credentials',
                'status' : 404
            }
            return Response(data=response)