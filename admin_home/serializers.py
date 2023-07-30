from rest_framework import serializers
from accounts.models import Account
from home.models import Service
from counselor.models import CounselorProfile, CounselorExperience, CounselorEducation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone', 'role', 'profile_image', 'is_active']


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        # Exclude is_active from the fields to update
        validated_data.pop('is_active', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Exclude is_active from the fields to update
        validated_data.pop('is_active', None)
        return super().update(instance, validated_data)
