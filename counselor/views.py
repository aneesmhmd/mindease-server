from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import *
from accounts.serializers import UserSerializer, ProfilePictureUpdateSerializer
from accounts.models import Account
from .models import CounselorEducation, CounselorExperience, CounselorAccount
from accounts.token import create_jwt_pair_tokens
from home.models import Service
from home.serializers import ServicesSerializer

# Create your views here.


class CounselorLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active and \
                    user.is_staff and user.role == 'counselor':
                counselor = CounselorAccount.objects.get(counselor=user)
                tokens = create_jwt_pair_tokens(user, counselor)
                response = {'message': 'Login succesfull', 'token': tokens}
                return Response(
                    data=response,
                    status=status.HTTP_200_OK
                )

            else:
                response = {'message': 'You are not a counselor'}
                return Response(
                    data=response,
                    status=status.HTTP_401_UNAUTHORIZED
                )

        else:
            response = {'message': 'No active account with given credentials'}
            return Response(
                data=response,
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePassword(APIView):
    def post(self, request, id):
        try:
            user = Account.objects.get(id=id, role='counselor', is_active=True)
        except Account.DoesNotExist:
            return Response(
                data={'message': 'No active counselor'},
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


class CounselorProfile(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Account.objects.filter(role='counselor')
    serializer_class = UserSerializer
    lookup_field = 'id'


class UpdateCounselorProfile(UpdateAPIView):
    queryset = Account.objects.filter(role='counselor')
    serializer_class = UserSerializer
    lookup_field = 'id'


class UpdateCounselorProfilePicture(UpdateAPIView):
    queryset = Account.objects.filter(role='counselor')
    serializer_class = ProfilePictureUpdateSerializer
    lookup_field = 'id'


class DeleteCounselorProfilePicture(DestroyAPIView):
    queryset = Account.objects.filter(role='counselor')
    serializer_class = ProfilePictureUpdateSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.profile_image.delete()
        instance.profile_image = None
        instance.save()


class AddCounselorAccount(CreateAPIView):
    queryset = CounselorAccount.objects.all()
    serializer_class = AddCounselorAccountSerializer

    def perform_create(self, serializer):
        counselor_id = self.request.data.get('counselor')
        service_id = self.request.data.get('specialization')
        counselor = Account.objects.get(id=counselor_id)
        service = Service.objects.get(id=service_id)
        serializer.save(counselor=counselor, specialization=service)


class GetCounselorAccount(RetrieveAPIView):
    queryset = CounselorAccount.objects.all()
    serializer_class = CounselorAccountSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]


class UpdateCounselorAccounts(UpdateAPIView):
    queryset = CounselorAccount.objects.all()
    serializer_class = CounselorAccountSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save(is_verified=True)
        return super().perform_update(serializer)


class AddCounselorEducation(CreateAPIView):
    queryset = CounselorEducation.objects.all()
    serializer_class = AddEducationSerializer

    def perform_create(self, serializer):
        counselor_id = self.request.data.get('counselor')
        try:
            counselor = Account.objects.get(pk=counselor_id)
        except Account.DoesNotExist:
            return Response(
                data={'message': 'Counselor profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(counselor=counselor)


@api_view(['GET'])
def get_educational_details(request, id):
    try:
        educations = CounselorEducation.objects.filter(counselor__id=id)
        serializer = CounselorEducationSerializer(educations, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    except CounselorEducation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class AddCounselorExperience(CreateAPIView):
    queryset = CounselorExperience.objects.all()
    serializer_class = AddExperienceSerializer

    def perform_create(self, serializer):
        counselor_id = self.request.data.get('counselor')
        try:
            counselor = Account.objects.get(pk=counselor_id)
        except Account.DoesNotExist:
            return Response(
                data={'message': 'Counselor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(counselor=counselor)


@api_view(['GET'])
def get_experience_details(request, id):
    try:
        experiences = CounselorExperience.objects.filter(counselor__id=id)
        serializer = CounselorExperienceSerializer(experiences, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    except CounselorExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ListSpecializations(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
