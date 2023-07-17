from rest_framework import serializers
from . models import Account
from rest_framework.validators import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

        def create(self, validated_data):
            # hashing password
            password = validated_data.pop('password')

            print(password)

            user = super().create(validated_data)
            user.set_password(password)
            user.save()
            return user



class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
