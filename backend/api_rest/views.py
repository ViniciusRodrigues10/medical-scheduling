from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AdditionalInformation
from .serializers import (
    AdditionalInformationSerializer,
    LifeHabitsSerializer,
    MedicalHistorySerializer,
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

        try:
            additional_info = AdditionalInformation.objects.get(user=request.user)
            additional_info.completed_form = True
            additional_info.save()

        except AdditionalInformation.DoesNotExist:
            return Response(
                {"error": "Additional information not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

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
    appointment = AppointmentFacade
    return appointment.book(request)


@api_view(["DELETE"])
@login_required_custom
def delete_appointment(request):
    appoitment = AppointmentFacade
    return appoitment.delete(request)
