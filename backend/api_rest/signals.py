from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Appointment

channel_layer = get_channel_layer()


@receiver(post_save, sender=Appointment)
def appointment_saved(sender, instance, created, **kwargs):
    event = "Consulta marcada" if created else "Consulta alterada"
    appointment = {
        "id": instance.id_appointment,
        "patient": instance.id_patient.email,
        "doctor": instance.id_doctor.user.email,
        "date": instance.date.strftime("%Y-%m-%d"),
        "start_time": instance.start_time.strftime("%H:%M:%S"),
        "end_time": instance.end_time.strftime("%H:%M:%S"),
        "event": event,
    }
    async_to_sync(channel_layer.group_send)(
        "appointments", {"type": "send_appointment", "appointment": appointment}
    )
    print(f"{event} - {appointment}")


@receiver(post_delete, sender=Appointment)
def appointment_deleted(sender, instance, **kwargs):
    appointment = {
        "id": instance.id_appointment,
        "patient": instance.id_patient.email,
        "doctor": instance.id_doctor.user.email,
        "date": instance.date.strftime("%Y-%m-%d"),
        "start_time": instance.start_time.strftime("%H:%M:%S"),
        "end_time": instance.end_time.strftime("%H:%M:%S"),
        "event": "Consulta desmarcada",
    }
    async_to_sync(channel_layer.group_send)(
        "appointments", {"type": "send_appointment", "appointment": appointment}
    )
    print(f"Consulta desmarcada - {appointment}")
