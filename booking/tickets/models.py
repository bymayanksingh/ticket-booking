import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Status(models.IntegerChoices):
    """
    Status choices available for tickets
    """
    ACTIVE = 1
    EXPIRED = 2


class Movie(models.Model):
    """
    Movie class to handle movies model
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Slots(models.Model):
    """
    Slots class to handle slots model
    """

    time = models.TimeField()

    def __str__(self):
        return "slot @ " + str(self.time)


class Show(models.Model):
    """
    Show class to handle show model
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    total_tickets = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    def __str__(self):
        return self.movie.name


class Tickets(models.Model):
    """
    Tickets class to handle tickets model
    """
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=100)
    no_of_tickets = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    # suppose you want to change ticket slot
    show_time = models.ForeignKey(Slots, on_delete=models.CASCADE)
    booking_time = models.TimeField(auto_now=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return str(self.ticket_id)

    class Meta:
        ordering = ["-show_time"]
