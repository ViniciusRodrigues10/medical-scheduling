from datetime import datetime, timedelta, date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .command.views_command import BookAppointmentCommand, DeleteAppointmentCommand
from .models import Availability, Doctor, Appointment, MedicalHistory, CustomUser
from .serializers import (
    AdditionalInformationSerializer,
    LifeHabitsSerializer,
    MedicalHistorySerializer,
    AppointmentSerializer,
    DoctorSerializer,
)
from .facade.views_facade import (
    AppointmentFacade,
    AvailabilityFacade,
    UserPatientFacade,
    UserDoctorFacade,
    LoginFacade,
)
from .decorator.decorators import login_required_custom, log_request
from .singleton.singleton import RequestLogger

logger = RequestLogger()


@api_view(["POST"])
def register_patient_api(request):
    view_register_patient = UserPatientFacade
    return view_register_patient.register_patiene(request)


@api_view(["POST"])
@log_request(logger)
def login_api(request):
    view_login = LoginFacade
    return view_login.login(request)


@api_view(["GET"])
@login_required_custom
def get_user_data(request):
    data_user = UserPatientFacade
    return data_user.get_data(request)


@api_view(["PUT"])
@login_required_custom
def update_user_data(request):
    update_user = UserPatientFacade
    return update_user.update_data_user(request)


@api_view(["DELETE"])
@login_required_custom
def delete_user_account(request):
    delete_user = UserPatientFacade
    return delete_user.delete_account(request)


@api_view(["POST"])
@login_required_custom
def register_additional_information(request):
    data = request.data
    data["user"] = request.user.id_user

    serializer = AdditionalInformationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@login_required_custom
def create_medical_history(request):
    data = request.data
    data["id_user"] = request.user.id_user

    serializer = MedicalHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@login_required_custom
def create_life_habits(request):

    data = request.data
    data["id_user"] = request.user.id_user

    serializer = LifeHabitsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: Add restriction, only superuser and administrator can register doctors
@api_view(["POST"])
def register_doctor(request):
    doctor = UserDoctorFacade
    return doctor.regiter_doctor(request)


@api_view(["GET"])
@login_required_custom
def get_doctor_data(request):
    doctor = UserDoctorFacade
    return doctor.get_data(request)


@api_view(["PUT"])
@login_required_custom
def update_doctor_data(request):
    doctor = UserDoctorFacade
    return doctor.update_data_doctor(request)


# TODO: add restriction, only superuser and admin can delete doctors
@api_view(["DELETE"])
@login_required_custom
def delete_doctor_account(request):
    doctor = UserDoctorFacade
    return doctor.delete_account(request)


# TODO: possibly remove the GET
# add valid time checks, do not allow adding past days and times
@api_view(["GET", "POST"])
@login_required_custom
def availability_list_create(request):
    doctor = UserDoctorFacade
    return doctor.availability(request)


# TODO: When a user makes an appointment, you must update the availability list
@api_view(["GET"])
@login_required_custom
def availability_list(request):
    availability = AvailabilityFacade
    return availability.list_of_availability(request)


@api_view(["PUT"])
@login_required_custom
def update_availability(request):
    availability = AvailabilityFacade
    return availability.update(request)


@api_view(["DELETE"])
@login_required_custom
def delete_availability(request):
    availability = AvailabilityFacade
    return availability.delete(request)


@api_view(["POST"])
@login_required_custom
def book_appointment(request):
    command = BookAppointmentCommand(AppointmentFacade, request)
    return command.execute()


@api_view(["DELETE"])
@login_required_custom
def delete_appointment(request):
    command = DeleteAppointmentCommand(AppointmentFacade, request)
    return command.execute()


@api_view(["GET"])
def get_specialty(request):
    specialties = Doctor.objects.values_list("specialty", flat=True).distinct()
    return Response({"specialties": list(specialties)}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_specialty_schedule(request, specialty_name):
    try:
        doctors = Doctor.objects.filter(specialty=specialty_name)

        if not doctors.exists():
            return Response(
                {"error": "Specialty not found"}, status=status.HTTP_404_NOT_FOUND
            )

        available_slots = Availability.objects.filter(id_doctor__in=doctors)

        response_data = []

        for slot in available_slots:
            slot_date = slot.date
            current_start_time = datetime.combine(slot.date, slot.start_time)
            end_time = datetime.combine(slot.date, slot.end_time)

            while current_start_time < end_time and slot_date >= date.today():
                next_time = current_start_time + timedelta(minutes=30)
                if next_time > end_time:
                    break

                if current_start_time > datetime.now():
                    response_data.append(
                        {
                            "doctor_email": slot.id_doctor.user.email,
                            "doctor_first_name": slot.id_doctor.user.first_name,
                            "doctor_last_name": slot.id_doctor.user.last_name,
                            "date": slot.date,
                            "start_time": current_start_time.time().strftime(
                                "%H:%M:%S"
                            ),
                            "end_time": next_time.time().strftime("%H:%M:%S"),
                        }
                    )
                current_start_time = next_time

        return Response(response_data, status=status.HTTP_200_OK)

    except Doctor.DoesNotExist:
        return Response(
            {"error": "Specialty not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_doctor_appointments_scheduled(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(
            id_doctor=doctor, date__gt=datetime.now().date()
        ) | Appointment.objects.filter(
            id_doctor=doctor,
            date=datetime.now().date(),
            end_time__gt=datetime.now().time(),
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_user_appointments(request):
    try:
        user = request.user

        appointments = Appointment.objects.filter(
            id_patient=user, date__gt=datetime.now().date()
        ) | Appointment.objects.filter(
            id_patient=user,
            date=datetime.now().date(),
            end_time__gt=datetime.now().time(),
        )

        serialized_appointments = AppointmentSerializer(appointments, many=True).data

        return Response(serialized_appointments, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_user_past_appointments(request):
    try:
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        now_date = datetime.now().date()
        now_time = datetime.now().time()

        appointments = Appointment.objects.filter(
            id_patient=user, date__lt=now_date
        ) | Appointment.objects.filter(
            id_patient=user, date=now_date, end_time__lt=now_time
        )

        serialized_appointments = AppointmentSerializer(appointments, many=True).data

        return Response(serialized_appointments, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_main_data(request):
    try:
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        now_date = datetime.now().date()

        future_appointments_count = Appointment.objects.filter(
            id_patient=user, date__gte=now_date
        ).count()

        past_appointments_count = Appointment.objects.filter(
            id_patient=user, date__lt=now_date
        ).count()

        user_info = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": dict(user.GENDER_CHOICES).get(user.gender, "Unknown"),
            "user_type": dict(user.USER_TYPE_CHOICES).get(user.user_type, "Unknown"),
        }

        doctors_count = Doctor.objects.count()

        data = {
            "future_appointments": future_appointments_count,
            "past_appointments": past_appointments_count,
            "user_info": user_info,
            "doctors_count": doctors_count,
        }

        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_doctor_appointments_history(request):
    try:
        user = request.user
        doctor = Doctor.objects.get(user=user)

        if not user.is_authenticated:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        now_date = datetime.now().date()
        now_time = datetime.now().time()

        appointments = Appointment.objects.filter(
            id_doctor=doctor, date__lt=now_date
        ) | Appointment.objects.filter(
            id_doctor=doctor, date=now_date, end_time__lt=now_time
        )

        serialized_appointments = AppointmentSerializer(appointments, many=True).data

        return Response(serialized_appointments, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_patient_medical_history(request, user_id):
    try:
        try:
            user = CustomUser.objects.get(id_user=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            medical_history = MedicalHistory.objects.get(id_user=user)
        except MedicalHistory.DoesNotExist:
            return Response(
                {"error": "Medical history does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_medical_history = MedicalHistorySerializer(medical_history).data

        return Response(serialized_medical_history, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def list_doctor_informations(request):
    try:
        doctors = Doctor.objects.all()
        serialized_doctors = DoctorSerializer(doctors, many=True).data
        return Response(serialized_doctors, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
