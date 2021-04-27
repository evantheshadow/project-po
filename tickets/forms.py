from django import forms
# from django_select2.forms import Select2MultipleWidget, Select2Widget

import datetime
from .models import *

def get_cities():
    cities = City.objects.all()
    return tuple((city.id, city.name) for city in cities)
    # city_names = [
    #     _["name"] for _ in cities.order_by("name").values("name").distinct()
    # ]
    # city_names.sort()
    # return tuple((sup_name, sup_name) for sup_name in supplier_names)


class DateInput(forms.DateInput):
    input_type = 'date'


class ExampleForm(forms.Form):
    class Meta:
        fields = {"takeoff_place", "arrival_place", "my_date"}

    takeoff_place = forms.ChoiceField(
        label="Откуда",
        choices=tuple(),
        required=False,
        widget=forms.Select(choices=get_cities())
    )
    arrival_place = forms.ChoiceField(
        label="Куда",
        choices=tuple(),
        required=False,
        widget=forms.Select(choices=get_cities())
    )
    my_date = forms.DateField(
        label="Дата",
        required=False,
        widget=DateInput(), 
    )

    def __init__(self, request):
        super().__init__(request)
        print('Request Field: {}'.format(request))
        self.fields["takeoff_place"].choices = get_cities()
        self.fields["arrival_place"].choices = get_cities()

    def clean_takeoff_place(self):
        takeoff_place = self.cleaned_data["takeoff_place"]
        print('TOFF PLACE: {}'.format(takeoff_place))
        if isinstance(takeoff_place, str):
            if not takeoff_place.strip():
                print('TOFF PLACE1: {}'.format(takeoff_place))
                takeoff_place = None
        if takeoff_place:
            print('TOFF PLACE2: {}'.format(takeoff_place))
            takeoff_place = City.objects.filter(id=takeoff_place)
        return takeoff_place

    def clean_arrival_place(self):
        arrival_place = self.cleaned_data["arrival_place"]
        print('ARR PLACE: {}'.format(arrival_place))
        if isinstance(arrival_place, str):
            if not arrival_place.strip():
                arrival_place = None
        if arrival_place:
            arrival_place = City.objects.filter(id=arrival_place)
        return arrival_place

    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data

    # def save(self, *args, **kwargs):
    #     city = super().save(*args, **kwargs)
        
    #     for flights in self.available_flights:
    #         Flight.objects.filter(
    #             takeoff_place = takeoff_place,
    #             arrival_place = arrival_place,
    #             takeoff_time = date,
    #         )
    #     return city