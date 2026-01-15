from rest_framework import serializers
from .models import TestDriveAppointment, VehicleInformationRequest, VehicleInformation

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


def to_text_representation(instance):
    lines = []
    for field in instance._meta.fields:
        name = field.name
        value = getattr(instance, name)
        lines.append(f"{name}: {value}")
    return "\n".join(lines)