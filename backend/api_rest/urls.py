from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='user'),
    path('register/', views.register_api, name='register')
]