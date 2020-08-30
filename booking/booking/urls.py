"""booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import User
from tickets.models import Tickets, Movie
from rest_framework import routers
import uuid
from tickets.views import ShowViewSet, TicketsList, TicketsDetail, MovieViewSet, SlotsViewSet, TicketsForTime

router = routers.DefaultRouter()
router.register(r'api/movies', MovieViewSet) #1
router.register(r'api/slots', SlotsViewSet) #2
router.register(r'api/shows', ShowViewSet) #3


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/tickets/', TicketsList.as_view()),
    path(r'api/tickets/time/<int:show_time_id>', TicketsForTime.as_view()),
    path(r'api/tickets/<uuid:ticket_id>', TicketsDetail.as_view()),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
]
