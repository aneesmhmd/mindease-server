from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Account
from .serializers import UserSerializer

class UserProfile(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class ChangePassword(APIView):

    def post(self, request, id):
        user = Account.objects.get(id=id)
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if user is not None and user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(data={'message': 'Password reset succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'Invalid Old password'}, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateProfile(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = Account.objects.all()
    lookup_field = 'id'
