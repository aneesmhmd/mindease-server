from counselor.models import CounselorProfile
from accounts.models import Account
from accounts.serializers import UserRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class CounselorRegistration(APIView):
    def post(self, request):
        print(request.data['values'])
        serializer = UserRegisterSerializer(data=request.data['values'])
        # print(serializer)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.is_staff = True
            user.role = 'counselor'
            user.save()
            CounselorProfile.objects.create(counselor=user)

            return Response({'msg' : 'Account succesfully Created', 'status':200})
        return Response({'msg': 'Registration failed'})
    
