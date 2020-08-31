from datetime import datetime, time, timedelta
from tickets.models import Tickets, Status


def mark_deleted():
    try:
        b = datetime.time(datetime.now())
        a = timedelta(hours=8)
        t = b-a
        tickets = Tickets.objects.filter(booking_time=b-a)
        tickets.delete()
    except:
        pass

def mark_expired():
    try:
        b = datetime.time(datetime.now())
        a = timedelta(hours=8)
        tickets = Tickets.objects.filter(booking_time=b-a)
        
        for ticket in tickets.iterator:       
            ticket.status = Status.EXPIRED.value
            ticket.save()
    except:
        pass
