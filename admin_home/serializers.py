from rest_framework import serializers
from accounts.models import Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id' ,'first_name', 'last_name', 'email', 'phone', 'role', 'profile_image', 'is_active']