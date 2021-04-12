from django import forms
from django.db import models
from tickets.models import *


class AirportChoiceField(forms.Form):

    airports = forms.ModelChoiceField(
        queryset=Airport.objects.values_list("air_name", flat=True).distinct(),
        empty_label=None
    )