from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from counselor.models import CounselorAccount
from .serializers import *
from home.models import Service
from booking.models import *
from booking.serializers import *


# Create your views here.
class DashboardView(APIView):
    def get(self, request, format=None):
        users_count = Account.objects.filter(role='user').count()
        counselors_count = CounselorAccount.objects.all().count()
        services_count = Service.objects.all().count()
        tasks_count = PsychologicalTasks.objects.all().count()
        subscriptions_count = TaskSubscription.objects.all().count()
        appointments_count = Appointments.objects.all().count()

        data = {
            'users': users_count,
            'counselors': counselors_count,
            'services': services_count,
            'tasks': tasks_count,
            'subscriptions': subscriptions_count,
            'appointments': appointments_count
        }

        return Response(data)


class AddServices(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer

    def perform_create(self, serializer):
        title = self.request.data.get('title', None)
        if title and Service.objects.filter(title=title).exists():
            raise serializers.ValidationError('Title should be unique')
        serializer.save()


class ListServices(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Service.objects.all().order_by('-id')
    serializer_class = ServicesSerializer


class UpdateServices(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer


class DeleteServices(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer


class ManageServices(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        if instance.is_active:
            message = f'"{instance.title}" listed succesfully'
        else:
            message = f'"{instance.title}" unlisted succesfully'
        return Response(data={'message': message}, status=status.HTTP_200_OK)


class ListPsychologicalTasks(ListAPIView):
    queryset = PsychologicalTasks.objects.all().order_by('-id')
    serializer_class = PsychologicalTaskSerializer


class GetPyshcologicalTaskDetails(RetrieveAPIView):
    queryset = PsychologicalTasks.objects.all()
    serializer_class = PsychologicalTaskSerializer
    lookup_field = 'id'


class ListTaskItems(APIView):
    def get(self, request, id):
        task_items = TaskItems.objects.filter(task__id=id).order_by('id')
        serializer = TaskItemsSerializer(task_items, many=True)
        return Response(data=serializer.data)


class AddPsychologicalTasks(CreateAPIView):
    queryset = PsychologicalTasks.objects.all()
    serializer_class = PsychologicalTaskSerializer

    def perform_create(self, serializer):
        title = self.request.data.get('title', None)
        if title and PsychologicalTasks.objects.filter(title=title).exists():
            raise serializers.ValidationError('Title should be unique')
        serializer.save()


class AddTaskItems(CreateAPIView):
    queryset = TaskItems.objects.all()
    serializer_class = TaskItemsSerializer


class UpdatePsychologicalTasks(UpdateAPIView):
    queryset = PsychologicalTasks.objects.all()
    serializer_class = PsychologicalTaskSerializer
    lookup_field = 'id'


class UpdateTaskItems(UpdateAPIView):
    queryset = TaskItems.objects.all()
    serializer_class = TaskItemsSerializer
    lookup_field = 'id'


class ManagePsychologialTask(APIView):
    def patch(self, request, id):
        try:
            task = PsychologicalTasks.objects.get(id=id)
            task.is_active = not task.is_active
            task.save()
            if task.is_active:
                message = 'Task Listed!'
            else:
                message = 'Task Unlisted!'
            return Response(data={'message': message}, status=status.HTTP_200_OK)
        except PsychologicalTasks.DoesNotExist:
            return Response(data={'message': 'Invalid user'}, status=status.HTTP_404_NOT_FOUND)


class ListTaskSubscriptions(ListAPIView):
    queryset = TaskSubscription.objects.all().order_by('id')
    serializer_class = TaskSubscriptionSerialzer


class DeletePsychologicalTasks(DestroyAPIView):
    queryset = PsychologicalTasks.objects.all()
    serializer_class = PsychologicalTaskSerializer
    lookup_field = 'id'


class DeleteTaskItems(DestroyAPIView):
    queryset = TaskItems.objects.all()
    serializer_class = TaskItemsSerializer
    lookup_field = 'id'


class ListCallBackReqs(ListAPIView):
    queryset = CallBackReqs.objects.all().order_by('is_contacted', '-id')
    serializer_class = CallBackReqsSerializer


class UpdateCallBackReqs(UpdateAPIView):
    queryset = CallBackReqs.objects.all()
    serializer_class = CallBackReqsSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.is_contacted = not instance.is_contacted
        serializer.save()


class ListAllAppointments(ListAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentSerializer
