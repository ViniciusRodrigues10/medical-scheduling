from django.urls import path
from . import views

urlpatterns = [
    path('register-patient/', views.register_patient_api, name='register-patient'),
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='user'),
]
 