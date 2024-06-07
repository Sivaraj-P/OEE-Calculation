from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Machine,ProductionLog
from .serializers import MachineSerializer,ProductionLogSerializer
from datetime import datetime


class MachineAPIView(APIView):
    def get(self,request):
        try:
            machines=Machine.objects.all()
            serializer=MachineSerializer(machines,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OEECalculationAPIView(APIView):
    def get(self,request):
        try:
            machine_id = request.query_params.get('machine_id')
            from_date = request.query_params.get('from_date')
            to_date = request.query_params.get('to_date')

            filters = Q()
            if machine_id:
                filters &= Q(machine_id=machine_id)
            if from_date:
                filters &= Q(start_time__gte=datetime.strptime(from_date, '%Y-%m-%d'))
            if to_date:
                filters &= Q(end_time__lte=datetime.strptime(to_date, '%Y-%m-%d'))


            production_log=ProductionLog.objects.filter(filters)
            serializer=ProductionLogSerializer(production_log,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response( {'detail':'Something went wrong please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
