from django.contrib.auth import authenticate
import datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import *
from accounts.serializers import UserSerializer, ProfilePictureUpdateSerializer
from accounts.models import Account
from .models import *
from booking.models import *
from booking.serializers import *
from accounts.token import create_jwt_pair_tokens
from home.models import Service
from admin_home.serializers import ServicesSerializer

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
                tokens = create_jwt_pair_tokens(user, counselor.id)
                response = {'message': 'Login succesfull', 'token': tokens}
                return Response(
                    data=response,
                    status=status.HTTP_200_OK
                )

            else:
                response = {'message': 'Unauthorized user'}
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


class IsCounselorAuth(APIView):

    def get(self, request, id):
        try:
            counselor = Account.objects.get(
                id=id, is_active=True, role='counselor')
            return Response(data={'success': True}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(data={'failure': False}, status=status.HTTP_401_UNAUTHORIZED)


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


class ListSlots(APIView):
    def post(self, request, id):
        date = request.data.get('selectedDate')
        slots = TimeSlots.objects.filter(counselor__id=id, date=date)
        if slots.exists():
            serializer = TimeSlotSerializer(slots, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'message': 'Not found!'},
                status=status.HTTP_404_NOT_FOUND
            )


class AddSlots(APIView):
    def post(self, request, id):
        try:
            counselor = CounselorAccount.objects.get(id=id)
            date = request.data.get('selectedDate')
            time_slots = request.data.get('selectedTime')
            slot_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

            if TimeSlots.objects.filter(counselor=counselor, date=slot_date).exists():
                return Response(
                    data={'message': 'You have already added slots for selected date'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            slots = []
            for i in time_slots:
                slot_start = datetime.datetime.strptime(i, "%H:%M").time()
                slot_end = (datetime.datetime.combine(datetime.date(
                    1, 1, 1), slot_start) + datetime.timedelta(hours=1)).time()
                slot = TimeSlots(
                    counselor=counselor,
                    date=slot_date,
                    start=slot_start,
                    end=slot_end,
                )
                slots.append(slot)

            TimeSlots.objects.bulk_create(slots)
            return Response(
                data={'message': 'Slots added successfully'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={'message': 'Some error occured.Please try again!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ListAllAppointments(APIView):
    def get(self, request, id):
        current_date = datetime.datetime.now().date()
        appointments = Appointments.objects.filter(
            counselor__id=id, session_date=current_date, is_paid=True)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ShareMeetLink(CreateAPIView):
    queryset = MeetLink.objects.all()
    serializer_class = MeetLinkSerializer


class UpdateMeetLink(UpdateAPIView):
    queryset = MeetLink.objects.all()
    serializer_class = UpdateLinkSerializer


class ListAppointmentByDate(APIView):
    def get(self, request, id, date):
        appointments = Appointments.objects.filter(
            counselor__id=id, session_date=date, is_paid=True)

        if appointments.exists():
            serializer = AppointmentSerializer(appointments, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={'message': 'No appointments on the selected date'},
            status=status.HTTP_200_OK
        )


class UpdateAppointmentStatus(APIView):
    def patch(self, request, id):
        try:
            app_status = request.data.get('status')
            appointment = Appointments.objects.get(id=id, status='Pending')
            appointment.status = app_status
            appointment.save()

            link = MeetLink.objects.get(appointment=appointment)
            link.delete()
            return Response(status=status.HTTP_200_OK)

        except Appointments.DoesNotExist:
            return Response(
                data={'message': 'Appointment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except MeetLink.DoesNotExist:
            return Response(status=status.HTTP_200_OK)
