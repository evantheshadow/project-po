from django.conf.urls import url, include
from .views import AirportListView

app_name = "tickets"

urlpatterns = [
    url(
        r'^',
        AirportListView.as_view(),
    ),
]