from django.conf.urls import url, include
from django.urls import path
from .views import *

app_name = "tickets"

urlpatterns = [
    path(
        '',
        CityListView.as_view(),
        name='home'
    ),
    # path(
    #     'thanks/',
    #     AirportListView.as_view(),
    #     name='thanks',
    # ),
    path(
        'flights/',
        SearchListView.as_view(),
        name='flights',
    ),
]