from django.db import models

class TestDriveAppointment(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    date = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=30, blank=True, null=True)
    transmission = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=60, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.date} {self.time}"


class VehicleInformationRequest(models.Model):
    make = models.CharField(max_length=60, blank=True)
    model = models.CharField(max_length=60, blank=True)
    budget = models.CharField(max_length=20, blank=True)
    body_type = models.CharField(max_length=60, blank=True)
    fuel_type = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=15, blank=True)
    mileage = models.CharField(max_length=10, blank=True)