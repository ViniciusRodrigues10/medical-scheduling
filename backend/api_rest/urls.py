from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path("register-patient/", views.register_patient_api, name="register-patient"),
    path("register-doctor/", views.register_doctor, name="register-doctor"),
    path("login/", views.login_api, name="login"),
    path("user/", views.get_user_data, name="user"),
    path("user-doctor/", views.get_doctor_data, name="user-doctor"),
    path("update-user/", views.update_user_data, name="update-user"),
    path("user-doctor/update-doctor", views.update_doctor_data, name="update-doctor"),
    path("logout/", knox_views.LogoutView.as_view()),
    path("logoutall", knox_views.LogoutAllView.as_view()),
    path("delete-account/", views.delete_user_account, name="delete-account"),
    path("delete-doctor/", views.delete_doctor_account, name="delete-doctor"),
    path("delete-appointment/", views.delete_appointment, name="delete-appointment"),
    path(
        "availability-list-create/",
        views.availability_list_create,
        name="availability-list-create",
    ),
    path("availability-list/", views.availability_list),
    path("update-availability/", views.update_availability, name="update-availability"),
    path("availability/delete/", views.delete_availability, name="delete-availability"),
    path("appointment/book/", views.book_appointment, name="book-appointment"),
    path(
        "medical-history/", views.create_medical_history, name="create-medical-history"
    ),
    path("life-habits/", views.create_life_habits, name="create-life-habits"),
    path(
        "additional-information/",
        views.register_additional_information,
        name="additional-information",
    ),
    path("specialties/", views.get_specialty, name="specialties"),
    path(
        "availability/<str:specialty_name>/",
        views.get_specialty_schedule,
        name="available_slots_by_specialty",
    ),
    path(
        "doctor-appointments/",
        views.get_doctor_appointments_scheduled,
        name="doctor-appointments",
    ),
    path(
        "user/appointments/",
        views.get_user_appointments,
        name="get-user-appointments",
    ),
]
