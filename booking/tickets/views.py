from django.http import Http404
from django.shortcuts import render
from rest_framework import routers, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import Movie, Show, Slots, Tickets
from tickets.serializers import (
    MovieSerializer,
    ShowSerializer,
    SlotsSerializer,
    TicketsSerializer,
)


def get_show(show_id):
    """
    Args: show_id

    ReturnObject: Show class object

    Raise: Http404 when Show object is not availble
    correspoding to the given show_id
    """
    try:
        return Show.objects.get(id=show_id)
    except Tickets.DoesNotExist:
        raise Http404


def update_show_ticket_count(show_id, booked_tickets_count):
    """
    Args: show_id, booked_tickets_count

    Description: this method updates & saves the available ticktes
    in Shows by decrementing booked ticket count from total show tickets     
    """
    show = get_show(show_id)
    show.total_tickets = show.total_tickets - booked_tickets_count
    show.save()


class TicketsForTime(APIView):
    """
    This class helps in implementing GET api/tickets/{show_time_id}
    for given time, return all the tickets and the corresponding 
    users
    """
    def get_object(self, show_time_id):
        """
        Args: show_time_id

        ReturnObject: Ticket class object according to filtered show_time_id

        Raise: Http404 when Ticket object is not availble
        correspoding to the given show_time_id
        """
        try:
            return Tickets.objects.filter(show_time=show_time_id)
        except Tickets.DoesNotExist:
            raise Http404

    def get(self, request, show_time_id):
        """
        Args: http request object, show_time_id

        Return: Response object  according to filtered show_time_id
        """
        ticket = self.get_object(show_time_id)
        serializer = TicketsSerializer(ticket, many=True, context={"request": request})
        return Response(serializer.data)


class ShowViewSet(viewsets.ModelViewSet):
    """
    Model View Set Class which abstracting the various http methods
    and endpoints into a viewset
    """
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class TicketsList(APIView):
    """List all the movie tickets, create new tickets"""

    def get(self, request, format=None):
        """
        Args: http request object

        Returns: Response object containing list of movie tickets
        """
        tickets = Tickets.objects.all()
        serializer = TicketsSerializer(tickets, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Args: http request object

        Description: handles ticket counts business logic and 
        booking of new ticket.

        Returns: Response object which returns the succesfully 
        created ticket
        """

        serializer = TicketsSerializer(data=request.data, context={"request": request})

        booked_tickets_count = request.data["no_of_tickets"]
        show_id = int(
            request.data["show"]
            .split("http://127.0.0.1:8000/api/shows/")[-1]
            .split("/")[0]
        )

        if booked_tickets_count > get_show(show_id).total_tickets:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        update_show_ticket_count(show_id, booked_tickets_count)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketsDetail(APIView):
    """
    Retrieve, update or delete a ticket instance.
    """

    def get_object(self, ticket_id):
        """
        Args: ticket_id

        ReturnObject: Ticket class object according to  ticket_id

        Raise: Http404 when Ticket object is not availble
        correspoding to the given ticket_id
        """
        
        try:
            return Tickets.objects.get(ticket_id=ticket_id)
        except Tickets.DoesNotExist:
            raise Http404

    def get(self, request, ticket_id, format=None):
        """
        handles get request for ticket instance
        """

        ticket = self.get_object(ticket_id)
        serializer = TicketsSerializer(ticket, context={"request": request})
        return Response(serializer.data)

    def put(self, request, ticket_id, format=None):
        """
        handle put request for ticket instance
        """
        
        ticket = self.get_object(ticket_id)
        serializer = TicketsSerializer(
            ticket, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticket_id, format=None):
        """
        handles delete request for ticket instance
        """

        ticket = self.get_object(ticket_id)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlotsViewSet(viewsets.ModelViewSet):
    """
    Retrieve, update or delete Slots.
    """
    queryset = Slots.objects.all()
    serializer_class = SlotsSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
