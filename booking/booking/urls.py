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
import uuid

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from tickets.models import Movie, Tickets
from tickets.views import (
    MovieViewSet,
    ShowViewSet,
    SlotsViewSet,
    TicketsDetail,
    TicketsForTime,
    TicketsList,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Ticket Booking API",
        default_version="v1",
        description="Ticket booking API-Zomentum",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"api/movies", MovieViewSet)  # 1
router.register(r"api/slots", SlotsViewSet)  # 2
router.register(r"api/shows", ShowViewSet)  # 3


urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"", include(router.urls)),
    url(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(r"api/tickets/", TicketsList.as_view()),
    path(r"api/tickets/time/<int:show_time_id>", TicketsForTime.as_view()),
    path(r"api/tickets/<uuid:ticket_id>", TicketsDetail.as_view()),
    path(r"api/", include("rest_framework.urls", namespace="rest_framework")),
]
