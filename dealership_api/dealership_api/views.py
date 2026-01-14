from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dealership_api.dealership_api.serialiers import TestDriveAppointmentSerializer


@api_view(["POST"])
def create_test_drive(request):
    # Accept from query params per spec ("in": "query")
    # Example: POST /api/test-drives/?name=...&phone=...&date=2026-01-20&time=14:30
    data = request.query_params.dict()
    serializer = TestDriveAppointmentSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(TestDriveAppointmentSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
