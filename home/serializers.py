from admin_home.serializers import PsychologicalTaskSerializer, TaskItems
from rest_framework.serializers import ModelSerializer
from .models import TaskSubscription


class CreateTaskSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = TaskSubscription
        fields = '__all__'


class RetrieveTaskItemsSerializer(ModelSerializer):
    task = PsychologicalTaskSerializer()

    class Meta:
        model = TaskItems
        fields = '__all__'
