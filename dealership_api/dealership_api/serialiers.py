from rest_framework import serializers
from .models import TestDriveAppointment
from datetime import datetime

class TestDriveAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestDriveAppointment
        fields = [
            "id",
            "name",          # string
            "phone",         # string
            "date",          # string (YYYY-MM-DD)
            "time",          # string (HH:MM)
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

    def validate_date(self, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise serializers.ValidationError("Use YYYY-MM-DD for date.")
        return value

    def validate_time(self, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%H:%M").time()
            except ValueError:
                raise serializers.ValidationError("Use HH:MM (24-hour) for time.")
        return value
