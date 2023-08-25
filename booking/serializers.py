from rest_framework.serializers import ModelSerializer
from .models import *
from counselor.serializers import CounselorAccountSerializer
from accounts.serializers import UserSerializer


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = '__all__'


class AppointmentSerializer(ModelSerializer):
    slot = TimeSlotSerializer()
    counselor = CounselorAccountSerializer()
    user = UserSerializer()

    class Meta:
        model = Appointments
        fields = '__all__'


class MeetLinkSerializer(ModelSerializer):
    class Meta:
        model = MeetLink
        fields = '__all__'
