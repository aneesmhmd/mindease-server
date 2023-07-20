from rest_framework import serializers
from . models import Account
from rest_framework.validators import ValidationError

class CounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


