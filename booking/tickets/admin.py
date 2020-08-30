from django.contrib import admin

from .models import Movie, Show, Slots, Tickets

# Register your models here.
admin.site.register(Tickets)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Slots)
