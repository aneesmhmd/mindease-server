from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Service
from .serializers import ServicesListSerializer
# Create your views here.
class GetServicesList(APIView):
    def get(self,request):
        services = Service.objects.all()
        serializer = ServicesListSerializer(services,many=True)
        return Response(serializer.data)
