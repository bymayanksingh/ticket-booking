from datetime import datetime, time
from tickets.models import Tickets, Status

def mark_expired():
    print("running")
    tickets = Tickets.objects.all()
    for ticket in tickets:
        b = datetime.time(datetime.now())
        a = ticket.booking_time
        diff = datetime.combine(datetime.today(), b) - datetime.combine(datetime.today(),a)
        if diff.seconds >= 28800:
            ticket.status = Status.EXPIRED.value
            ticket.save()
