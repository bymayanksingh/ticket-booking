from rest_framework import serializers

from tickets.models import Movie, Show, Slots, Tickets


class SlotsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Slots
        fields = ("time",)


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ("name",)


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = (
            "movie",
            "total_tickets",
        )


class TicketsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tickets
        fields = (
            "ticket_id",
            "user_name",
            "phone_no",
            "show",
            "no_of_tickets",
            "show_time",
            "booking_time",
            "status",
        )
