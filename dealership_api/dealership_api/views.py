from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import TestDriveAppointment
from datetime import datetime

from dealership_api.models import TestDriveAppointment
from dealership_api.serialiers import TestDriveAppointmentSerializer
from rest_framework.views import APIView

from .serialiers import VehicleInformationRequestSerializer


class ScheduleTestDriveView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = TestDriveAppointmentSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response("Successfully created new test drive appointment with the following data: " + str(TestDriveAppointmentSerializer(instance).data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        qs = TestDriveAppointment.objects.all()
        serializer = TestDriveAppointmentSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleInformationView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = VehicleInformationRequestSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response("Successfully submitted request for vehicle information with the following data: " + str(
                VehicleInformationRequestSerializer(instance).data), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

