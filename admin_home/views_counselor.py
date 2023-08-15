from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView

from accounts.models import Account
from .serializers import UserSerializer
from counselor.models import CounselorAccount, CounselorEducation, CounselorExperience
from counselor.serializers import CounselorEducationSerializer, CounselorExperienceSerializer


class ListCounselors(ListAPIView):
    queryset = Account.objects.filter(
        role='counselor', is_staff=True).exclude(is_admin=True).order_by('-id')
    serializer_class = UserSerializer


class ManageCounselor(APIView):
    def patch(self, request, pk):
        try:
            user = Account.objects.get(
                id=pk, role='counselor', is_staff=True, is_admin=False)
            user.is_active = not user.is_active
            user.save()
            if user.is_active:
                message = 'Counselor Unblocked'
            else:
                message = 'Counselor blocked'
            return Response(data={'message': message}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(data={'message': 'Invalid counselor'}, status=status.HTTP_404_NOT_FOUND)


class ListEducationRequests(ListAPIView):
    queryset = CounselorEducation.objects.filter(
        is_verified=False).order_by('-id')
    serializer_class = CounselorEducationSerializer


class ListExperienceRequests(ListAPIView):
    queryset = CounselorExperience.objects.filter(
        is_verified=False).order_by('-id')
    serializer_class = CounselorExperienceSerializer


class GetEducationDetails(RetrieveAPIView):
    queryset = CounselorEducation.objects.all()
    serializer_class = CounselorEducationSerializer
    lookup_field = 'id'


class GetExperienceDetails(RetrieveAPIView):
    queryset = CounselorExperience.objects.filter(is_verified=False)
    serializer_class = CounselorExperienceSerializer
    lookup_field = 'id'


@api_view(['PATCH'])
def verify_education_requests(request, id):
    try:
        education = CounselorEducation.objects.get(id=id)
        education.is_verified = True
        education.save()
        return Response(
            data={'message': 'Education request verified'},
            status=status.HTTP_200_OK
        )
    except CounselorEducation.DoesNotExist:
        return Response(
            data={'message': 'Education request not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def verify_experience_requests(request, id):
    try:
        experience = CounselorExperience.objects.get(id=id)
        experience.is_verified = True
        experience.save()
        return Response(
            data={'message': 'Education request verified'},
            status=status.HTTP_200_OK
        )
    except CounselorEducation.DoesNotExist:
        return Response(
            data={'message': 'Education request not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class DeclineEducationRequest(DestroyAPIView):
    queryset = CounselorEducation.objects.filter(is_verified=False)
    serializer_class = CounselorEducationSerializer
    lookup_field = 'id'


class DeclineExperienceRequest(DestroyAPIView):
    queryset = CounselorExperience.objects.filter(is_verified=False)
    serializer_class = CounselorExperienceSerializer
    lookup_field = 'id'
