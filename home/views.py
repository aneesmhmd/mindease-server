from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Service
from .serializers import ServicesListSerializer
# Create your views here.


class GetServicesList(APIView):
    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServicesListSerializer(services, many=True)
        return Response(serializer.data)
