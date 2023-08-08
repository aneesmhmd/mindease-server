from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import ServicesSerializer, Service
from counselor.serializers import CounselorAccountSerializer, CounselorAccount, CounselorEducation, CounselorEducationSerializer
from admin_home.serializers import PsychologicalTaskSerializer, PsychologicalTasks
# Create your views here.


class GetServicesList(APIView):
    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)


class ListCounselors(ListAPIView):
    queryset = CounselorAccount.objects.filter(is_verified=True)
    serializer_class = CounselorAccountSerializer


class ListPsychologicalTasks(ListAPIView):
    queryset = PsychologicalTasks.objects.filter(is_active=True)
    serializer_class = PsychologicalTaskSerializer


class GetPsychologistDetails(RetrieveAPIView):
    queryset = CounselorAccount.objects.filter(is_verified=True)
    serializer_class = CounselorAccountSerializer
    lookup_field = 'id'