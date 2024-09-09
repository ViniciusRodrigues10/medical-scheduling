class BookAppointmentCommand:
    def __init__(self, appointment_facade, request):
        self.appointment_facade = appointment_facade
        self.request = request

    def execute(self):
        return self.appointment_facade.book(self.request)


class DeleteAppointmentCommand:
    def __init__(self, appointment_facade, request):
        self.appointment_facade = appointment_facade
        self.request = request

    def execute(self):
        return self.appointment_facade.delete(self.request)
