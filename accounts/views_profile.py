from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Account
from .serializers import UserSerializer, ProfilePictureUpdateSerializer


class UserProfile(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class ChangePassword(APIView):

    def post(self, request, id):
        user = Account.objects.get(id=id, role='user', is_active=True)
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if user is not None and user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return Response(data={'message': 'Password reset succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'Invalid Old password'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserProfile(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = Account.objects.filter(role='user')
    lookup_field = 'id'


class UpdateUserProfilePhoto(UpdateAPIView):
    queryset = Account.objects.filter(role='user')
    serializer_class = ProfilePictureUpdateSerializer
    lookup_field = 'id'


class RemoveUserProfilePhoto(DestroyAPIView):
    serializer_class = ProfilePictureUpdateSerializer
    queryset = Account.objects.filter(role='user')
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Delete the profile image from the storage
        instance.profile_image.delete()
        # Set the profile_image field to null in the database
        instance.profile_image = None
        instance.save()
