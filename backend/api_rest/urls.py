from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('register-patient/', views.register_patient_api, name='register-patient'),
    path('register-doctor/', views.register_doctor, name='register-doctor'),
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='user'),
    path('user-doctor/', views.get_doctor_data, name='user-doctor'),
    path('update-user/', views.update_user_data, name='update-user'),
    path('user-doctor/update-doctor', views.update_doctor_data, name='update-doctor'),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall', knox_views.LogoutAllView.as_view()),
    path('delete-account/', views.delete_user_account, name='delete-account'),
    
]
 