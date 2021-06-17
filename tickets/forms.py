import datetime as dt
from datetime import datetime
# from django_select2.forms import Select2Widget

from django import forms
from .models import *

def get_cities():
    cities = City.objects.all()
    return tuple((city.id, city.name) for city in cities)


class DateInput(forms.DateInput):
    input_type = 'date'


class CityManagerForm(forms.Form):
    class Meta:
        fields = {"takeoff_place", "arrival_place", "my_date"}

    takeoff_place = forms.ChoiceField(
        label="Откуда",
        choices=get_cities(),
        required=False,
        widget=forms.Select(choices=get_cities())
    )
    arrival_place = forms.ChoiceField(
        label="Куда",
        choices=get_cities(),
        required=False,
        widget=forms.Select(choices=get_cities())
    )
    my_date = forms.DateField(
        label="Дата",
        required=True,
        widget=DateInput(), 
    )

    def __init__(self, request, *args, **kwargs):
        super(CityManagerForm, self).__init__(request)
        self.fields['my_date'].error_messages = {'required': ' '}

    def clean_takeoff_place(self):
        takeoff_place = self.cleaned_data["takeoff_place"]
        if isinstance(takeoff_place, str):
            if not takeoff_place.strip():
                takeoff_place = None
        if takeoff_place:
            takeoff_place = City.objects.filter(id=takeoff_place)
        return takeoff_place

    def clean_arrival_place(self):
        arrival_place = self.cleaned_data["arrival_place"]
        if isinstance(arrival_place, str):
            if not arrival_place.strip():
                arrival_place = None
        if arrival_place:
            arrival_place = City.objects.filter(id=arrival_place)
        return arrival_place

    def clean(self):
        cleaned_data = super(CityManagerForm, self).clean()
        my_date = str(cleaned_data.get('my_date'))
        if my_date == None:
            my_date_time = datetime.datetime.strptime(my_date, '%Y-%m-%d').date()
            if datetime.datetime.now().date() <= my_date_time:
                msg = u"Wrong Date Time!"
                self.add_error('my_date', msg)
        return cleaned_data