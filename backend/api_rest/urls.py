from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='user'),
    path('register_patient/', views.register_client_api, name='register_patient'),
    path('register_doctor/', views.register_doctor_api, name='register_doctor'),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall', knox_views.LogoutAllView.as_view())
]