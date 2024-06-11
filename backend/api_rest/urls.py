from django.urls import path
from . import views

urlpatterns = [
    path('register-patient/', views.register_patient_api, name='register-patient'),
]
