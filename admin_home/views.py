from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from counselor.models import CounselorProfile
from .serializers import ServicesSerializer
from home.models import Service


# Create your views here.
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
        print('Eneted here')

        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        print('Instance is not active:', instance.is_active)
        if instance.is_active:
            message = f'"{instance.title}" listed succesfully'
        else:
            message = f'"{instance.title}" unlisted succesfully'
        return Response(data={'message': message}, status=status.HTTP_200_OK)
