import re
from rest_framework import serializers
from . models import Account
from rest_framework.validators import ValidationError
from counselor.models import CounselorAccount
from django.forms.models import model_to_dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

        def validate(self, attrs):
            email_exist = Account.objects.filter(email=attrs['email']).exists()
            # Email validation
            if email_exist:
                return ValidationError('This email is already exist')
            return super().validate(attrs)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if not user.is_active:
            raise ValidationError('User is not active', code='inactive_user')

        if not user.is_admin and user.is_staff:
            counselor = CounselorAccount.objects.get(counselor=user)
            token['counselor'] = model_to_dict(counselor)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['is_active'] = user.is_active

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone', 'profile_image']

    def update(self, instance, validated_data):
        validated_data.pop('profile_image', None)
        return super().update(instance, validated_data)


class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile_image']