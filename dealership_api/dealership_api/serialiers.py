from rest_framework import serializers
from .models import TestDriveAppointment, VehicleInformationRequest
from datetime import datetime

class TestDriveAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestDriveAppointment
        fields = [
            "id",
            "name",          # string
            "phone",         # string
            "date",          # string
            "time",          # string
            "make",          # string
            "model",         # string
            "condition",     # string
            "transmission",  # string
            "location",      # string
            "created_at",
        ]

    extra_kwargs = {
        "name": {"required": True},
        "phone": {"required": True},
        "date": {"required": True},
        "time": {"required": True},
    }

class VehicleInformationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInformationRequest
        fields = '__all__'