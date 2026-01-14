
from django.contrib import admin
from django.urls import path

from dealership_api.views import ScheduleTestDriveView, VehicleInformationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/scheduletestdrive/', ScheduleTestDriveView.as_view(), name='create-test-drive'),
    path('api/vehicleinformation/', VehicleInformationView.as_view(), name='create-test-drive'),
]
