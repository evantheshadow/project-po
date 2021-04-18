from django.conf.urls import url, include
from .views import *

app_name = "tickets"

urlpatterns = [
    url(
        r'^',
        FlightListView.as_view(),
    ),
]