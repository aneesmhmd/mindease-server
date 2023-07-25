from rest_framework import serializers
from accounts.models import Account
from  home.models import Service
from counselor.models import CounselorProfile, CounselorExperience, CounselorEducation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id' ,'first_name', 'last_name', 'email', 'phone', 'role', 'profile_image', 'is_active']


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

