from rest_framework.serializers import ModelSerializer
from .models import *


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlots
        fields = '__all__'