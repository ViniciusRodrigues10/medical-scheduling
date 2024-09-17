from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/appointments/", consumers.AppointmentConsumer.as_asgi()),
]
