from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Doctor, Availability, Appointment
from datetime import datetime, timedelta
from django.db.models import Q
from .serializers import (
    AvailabilitySerializer,
    UpdateAvailabilitySerializer,
    AppointmentSerializer,
)
from .facade.views_facade import (
    AppointmentFacade,
    AvailabilityFacade,
    UserPatientFacade,
    UserDoctorFacade,
    LoginFacade,
)


@api_view(["POST"])
def register_patient_api(request):
    view_register_patient = UserPatientFacade
    return view_register_patient.register_patiene(request)


@api_view(["POST"])
def login_api(request):
    view_login = LoginFacade
    return view_login.login(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    data_user = UserPatientFacade
    return data_user.get_data(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_data(request):
    update_user = UserPatientFacade
    return update_user.update_data_user(request)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    delete_user = UserPatientFacade
    return delete_user.delete_account(request)


# TODO: Add restriction, only superuser and administrator can register doctors
@api_view(["POST"])
def register_doctor(request):
    doctor = UserDoctorFacade
    return doctor.regiter_doctor(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_data(request):
    doctor = UserDoctorFacade
    return doctor.get_data(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_doctor_data(request):
    doctor = UserDoctorFacade
    return doctor.update_data_doctor(request)


# TODO: add restriction, only superuser and admin can delete doctors
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_doctor_account(request):
    doctor = UserDoctorFacade
    return doctor.delete_account(request)


# TODO: possibly remove the GET
# add valid time checks, do not allow adding past days and times
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def availability_list_create(request):
    doctor = UserDoctorFacade
    return doctor.availability(request)


# TODO: When a user makes an appointment, you must update the availability list
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def availability_list(request):
    availability = AvailabilityFacade
    return availability.list_of_availability(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_availability(request):
    availability = AvailabilityFacade
    return availability.update(request)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_availability(request):
    availability = AvailabilityFacade
    return availability.delete(request)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    appointment = AppointmentFacade
    return appointment.book(request)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_appointment(request):
    appoitment = AppointmentFacade
    return appoitment.delete(request)
