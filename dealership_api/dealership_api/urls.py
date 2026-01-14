
from django.contrib import admin
from django.urls import path

from dealership_api.dealership_api.views import create_test_drive

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/test-drives/', create_test_drive, name='create-test-drive'),
]
