from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from ..models import Appointment, CustomUser, Doctor, Availability
from django.db.models import Q
from ..singleton.singleton import SingletonMeta
from ..serializers import (
    AdditionalInformationSerializer,
    AppointmentSerializer,
    CustomUserSerializer,
    EmailAuthTokenSerializer,
    UpdateAvailabilitySerializer,
    UpdateUserSerializer,
    DoctorSerializer,
    AvailabilitySerializer,
)
from ..singleton.singleton import RequestLogger
from ..decorator.decorators import log_request

logger = RequestLogger()


class UserPatientFacade(metaclass=SingletonMeta):
    def register_patiene(request):
        data = request.data.copy()
        data["user_type"] = 1

        serializer = CustomUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response(
            {
                "user_info": {
                    "id_user": user.id_user,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": user.gender,
                    "user_type": user.user_type,
                },
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )

    def get_data(request):
        user = request.user

        return Response(
            {
                "user_info": {
                    "id": user.id_user,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": user.gender,
                },
            },
            status=status.HTTP_200_OK,
        )

    def update_data_user(request):
        try:
            user = request.user
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = UpdateUserSerializer(
                user, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_account(request):
        try:
            user = request.user
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDoctorFacade(metaclass=SingletonMeta):
    def regiter_doctor(request):
        data = request.data.copy()
        user_data = {
            "email": data.get("email"),
            "password": data.get("password"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "gender": data.get("gender"),
            "user_type": 2,
        }

        additional_info_data = {
            "telephone": data.get("telephone"),
            "date_of_birth": data.get("date_of_birth"),
            "is_staff": True,
        }

        doctor_data = {
            "specialty": data.get("specialty"),
            "crm": data.get("crm"),
            "biography": data.get("biography"),
        }

        user_serializer = CustomUserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        additional_info_data["user"] = user.id_user

        additional_info_serializer = AdditionalInformationSerializer(
            data=additional_info_data
        )
        if additional_info_serializer.is_valid():
            additional_info = additional_info_serializer.save()
        else:
            user.delete()
            return Response(
                additional_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        doctor_data["user"] = user.id_user
        doctor_data["additional_info"] = additional_info.id
        doctor_serializer = DoctorSerializer(data=doctor_data)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
        else:

            additional_info.delete()
            user.delete()
            return Response(
                doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_data(request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "user_info": {
                    "id_user": doctor.user.id_user,
                    "email": doctor.user.email,
                    "first_name": doctor.user.first_name,
                    "last_name": doctor.user.last_name,
                    "gender": doctor.user.gender,
                    "user_type": doctor.user.user_type,
                },
                "additional_info": {
                    "telephone": doctor.user.additional_info.telephone,
                    "date_of_birth": doctor.user.additional_info.date_of_birth,
                },
                "doctor_info": {
                    "specialty": doctor.specialty,
                    "crm": doctor.crm,
                    "biography": doctor.biography,
                },
            },
            status=status.HTTP_200_OK,
        )

    def update_data_doctor(request):
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        user_data = {
            "email": data.get("email", doctor.user.email),
            "first_name": data.get("first_name", doctor.user.first_name),
            "last_name": data.get("last_name", doctor.user.last_name),
            "gender": data.get("gender", doctor.user.gender),
            "is_staff": data.get("is_staff", doctor.user.is_staff),
            "is_superuser": doctor.user.is_superuser,
            "is_active": doctor.user.is_active,
            "user_type": doctor.user.user_type,
        }

        additional_info_data = {
            "telephone": data.get("telephone", doctor.user.additional_info.telephone),
            "date_of_birth": data.get(
                "date_of_birth", doctor.user.additional_info.date_of_birth
            ),
            "completed_form": doctor.user.additional_info.completed_form,
        }

        doctor_data = {
            "specialty": data.get("specialty", doctor.specialty),
            "crm": data.get("crm", doctor.crm),
            "biography": data.get("biography", doctor.biography),
        }

        user_serializer = CustomUserSerializer(
            doctor.user, data=user_data, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        additional_info_serializer = AdditionalInformationSerializer(
            doctor.user.additional_info, data=additional_info_data, partial=True
        )
        if additional_info_serializer.is_valid():
            additional_info_serializer.save()
        else:
            return Response(
                additional_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        doctor_serializer = DoctorSerializer(doctor, data=doctor_data, partial=True)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return Response(doctor_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def delete_account(request):
        try:
            doctor = Doctor.objects.get(user=request.user)
            print("@@___id user: ", doctor.user)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = doctor.user
        doctor.delete()
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def availability(request):
        if request.method == "GET":
            user = request.user
            availabilities = Availability.objects.filter(id_professional__user=user)
            serializer = AvailabilitySerializer(availabilities, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            user = request.user
            print("USER: ", user)
            try:
                doctor = Doctor.objects.get(user=user)
            except Doctor.DoesNotExist:
                return Response(
                    {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
                )

            data = request.data.copy()
            data["id_doctor"] = doctor.pk

            serializer = AvailabilitySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginFacade(metaclass=SingletonMeta):
    @log_request(logger)
    def login(request):
        serializer = EmailAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        _, token = AuthToken.objects.create(user)

        return Response(
            {
                "user_info": {
                    "id_user": user.id_user,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": user.gender,
                    "user_type": user.user_type,
                },
                "token": token,
            },
            status=status.HTTP_200_OK,
        )


class AvailabilityFacade(metaclass=SingletonMeta):
    def list_of_availability(request):
        data = request.data.copy()
        doctor_name = data.get("doctor_name", None)
        specialty = data.get("specialty", None)

        availabilities = Availability.objects.all()

        if doctor_name:
            availabilities = availabilities.filter(
                Q(id_professional__user__first_name__icontains=doctor_name)
                | Q(id_professional__user__last_name__icontains=doctor_name)
            )

        if specialty:
            availabilities = availabilities.filter(
                Q(id_professional__specialty__icontains=specialty)
            )

        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

    def update(request):
        try:
            user = request.user
            doctor = Doctor.objects.get(user=user)
            date = request.data.get("date")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")

            availability = Availability.objects.get(
                id_professional=doctor,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
        except Availability.DoesNotExist:
            return Response(
                {"error": "Availability not found"}, status=status.HTTP_404_NOT_FOUND
            )

        update_data = {
            "date": request.data.get("new_date", availability.date),
            "start_time": request.data.get("new_start_time", availability.start_time),
            "end_time": request.data.get("new_end_time", availability.end_time),
        }

        serializer = UpdateAvailabilitySerializer(
            availability, data=update_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(request):
        try:
            user = request.user
            doctor = Doctor.objects.get(user=user)
            date = request.data.get("date")
            start_time = request.data.get("start_time")
            end_time = request.data.get("end_time")

            availability = Availability.objects.get(
                id_professional=doctor,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
        except Availability.DoesNotExist:
            return Response(
                {"error": "Availability not found"}, status=status.HTTP_404_NOT_FOUND
            )

        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentFacade:
    def book(request):
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
            return Response(
                {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            curret_date = datetime.today().date()
            current_time = datetime.now().time()

        except ValueError as e:
            return Response({"error: str(e)"}, status=status.HTTP_400_BAD_REQUEST)

        if date < curret_date:
            return Response(
                {"error": "Invalid date"}, status=status.HTTP_400_BAD_REQUEST
            )
        if date == curret_date and start_time < current_time:
            return Response(
                {"error": "Invalid time"}, status=status.HTTP_400_BAD_REQUEST
            )

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

    def delete(request):
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
                {"error": "Invalid date or time format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            appointment = Appointment.objects.get(
                id_user=user, date=date, start_time=start_time
            )
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
