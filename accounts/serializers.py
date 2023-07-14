from rest_framework import serializers
from . models import Account
from rest_framework.validators import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'