from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TestDriveAppointment, VehicleInformation
from .serialiers import TestDriveAppointmentSerializer, to_text_representation
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
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST);

        instance = serializer.save()
        print(data)
        car = VehicleInformation.objects.filter(make=data["make"], model=data["model"]).first()
        if not car:
            return Response("No vehicle found that matches your search criteria.", status=status.HTTP_200_OK)

        print(car)
        car_text = to_text_representation(car)
        print(car_text)
        return Response("We found a car that matches your criteria:\n" + str(car_text), status=status.HTTP_200_OK)

