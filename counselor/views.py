from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CounselorSerializer, CounselorEducationSerializer, CounselorExperienceSerializer
from accounts.models import Account
from .models import CounselorProfile, CounselorEducation, CounselorExperience
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
                    'token' : tokens,
                }

                return Response(data=response,status=status.HTTP_200_OK)
            else:
                response = {
                    'message' : 'You are not a counselor',
                }
                return Response(data=response,status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = {
                'message' : 'Invalid login credentials',
            }
            return Response(data=response,status=status.HTTP_404_NOT_FOUND)
        

class AddCounselorEducation(CreateAPIView):
    queryset = CounselorEducation.objects.all()
    serializer_class = CounselorEducationSerializer


class AddCounselorExperienceA(CreateAPIView):
    queryset = CounselorExperience.objects.all()
    serializer_class = CounselorExperienceSerializer
        