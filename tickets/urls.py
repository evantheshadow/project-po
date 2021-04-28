from django.conf.urls import url, include
from django.urls import path
from .views import *
from aviakassa.urls import *

app_name = "tickets"

urlpatterns = [
    url(
        r'^$',
        CityListView.as_view(),
        name='home'
    ),
    url(
        r'^flights/$',
        SearchListView.as_view(),
        name='flights',
    ),
    url(
        r'^flights/(?P<id>\d+)/$', 
        DetailFlightView.as_view(model=Flight), 
        name='flight_detail',
    ),
    url(
        r'^about/',
        AboutUsView.as_view(),
        name='about',
    ),
]

# (?P<id>\d+)/