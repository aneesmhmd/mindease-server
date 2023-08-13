from rest_framework import serializers
from accounts.models import Account
from home.models import *
from .models import *

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


class PsychologicalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalTasks
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('is_active', None)
        return super().create(validated_data)


class TaskItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItems
        fields = '__all__'


class CallBackReqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallBackReqs
        fields = '__all__'