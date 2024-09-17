import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("appointments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("appointments", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_appointment(self, event):
        appointment = event["appointment"]
        await self.send(text_data=json.dumps({"appointment": appointment}))
