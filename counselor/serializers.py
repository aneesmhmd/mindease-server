from rest_framework import serializers
from . models import Account, CounselorEducation, CounselorExperience, CounselorAccount
from rest_framework.validators import ValidationError
from booking.models import Appointments
from admin_home.serializers import ServicesSerializer

class CounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class AddCounselorAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorAccount
        fields = '__all__'


class CounselorAccountSerializer(serializers.ModelSerializer):
    counselor_details = CounselorSerializer(source='counselor', read_only=True)
    specialization_details = ServicesSerializer(
        source='specialization', read_only=True)

    class Meta:
        model = CounselorAccount
        fields = '__all__'


class AddEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorEducation
        fields = '__all__'


class AddExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselorExperience
        fields = '__all__'


class CounselorExperienceSerializer(serializers.ModelSerializer):
    counselor = CounselorSerializer()

    class Meta:
        model = CounselorExperience
        fields = '__all__'


class CounselorEducationSerializer(serializers.ModelSerializer):
    counselor = CounselorSerializer()

    class Meta:
        model = CounselorEducation
        fields = '__all__'


class UpdateAppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['status']
