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
    user = request.user
    doctor_first_name = request.data.get("doctor_first_name")
    doctor_last_name = request.data.get("doctor_last_name")
    date_str = request.data.get("date")
    start_time_str = request.data.get("start_time")

    if (
        not doctor_first_name
        or not doctor_last_name
        or not date_str
        or not start_time_str
    ):
        return Response(
            {
                "error": "Doctor's first name, last name, date, and start time are required"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        doctor = Doctor.objects.get(
            user__first_name=doctor_first_name, user__last_name=doctor_last_name
        )
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        curret_date = datetime.today().date()
        current_time = datetime.now().time()

    except ValueError as e:
        return Response({"error: str(e)"}, status=status.HTTP_400_BAD_REQUEST)

    if date < curret_date:
        return Response({"error": "Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
    if date == curret_date and start_time < current_time:
        return Response({"error": "Invalid time"}, status=status.HTTP_400_BAD_REQUEST)

    duration = timedelta(minutes=30)
    end_time = (datetime.combine(date, start_time) + duration).time()

    doctor_id = doctor.user.id_user
    appointment_exists = (
        Appointment.objects.filter(id_professional=doctor_id, date=date)
        .filter(start_time__lt=end_time, end_time__gt=start_time)
        .exists()
    )

    if appointment_exists:
        return Response(
            {"message": "The doctor is not available at the given date and time"},
            status=status.HTTP_200_OK,
        )

    appointment = Appointment(
        id_user=user,
        id_professional=doctor,
        date=date,
        start_time=start_time,
        end_time=end_time,
    )
    appointment.save()

    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_appointment(request):
    user = request.user
    date_str = request.data.get("date")
    start_time_str = request.data.get("start_time")

    if not date_str or not start_time_str:
        return Response(
            {"error": "Date and start time are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
    except ValueError:
        return Response(
            {"error": "Invalid date or time format"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        appointment = Appointment.objects.get(
            id_user=user, date=date, start_time=start_time
        )
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    appointment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
