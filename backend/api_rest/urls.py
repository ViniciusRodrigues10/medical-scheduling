from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('register-patient/', views.register_patient_api, name='register-patient'),
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='user'),
    path('update-user/', views.update_user_data, name='update-user'),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall', knox_views.LogoutAllView.as_view()),
    path('delete-account/', views.delete_user_account, name='delete-account'),
]
 