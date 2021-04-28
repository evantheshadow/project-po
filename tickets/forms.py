import datetime as dt
from datetime import datetime

from django import forms
from .models import *

def get_cities():
    cities = City.objects.all()
    return tuple((city.id, city.name) for city in cities)


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
        required=True,
        widget=DateInput(), 
    )

    def __init__(self, request, *args, **kwargs):
        super(ExampleForm, self).__init__(request)
        self.fields['my_date'].required = True
        self.fields['my_date'].error_messages = {'required': ' '}
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
        cleaned_data = super(ExampleForm, self).clean()
        my_date = str(cleaned_data.get('my_date'))
        print(my_date)
        if my_date == None:
            my_date_time = datetime.datetime.strptime(my_date, '%Y-%m-%d').date()
            if datetime.datetime.now().date() <= my_date_time:
                msg = u"Wrong Date Time!"
                self.add_error('my_date', msg)
        print(self.cleaned_data)
        return cleaned_data

class DetailForm(forms.Form):
    class Meta:
        fields = {"f_id"}

    f_id = forms.IntegerField(
        label="ID полета",
    )

    def __init__(self, request, *args, **kwargs):
        super(ExampleForm, self).__init__(request)

    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data


    # def clean(self):
    #     cleaned_data = super(DetailForm, self).clean()
    #     f_id = cleaned_data.get('f_id'))
    #     print(my_date)
    #     if f_id == None:
    #         msg = u"Wrong Date Time!"
    #         self.add_error('f_id', msg)
    #     print(self.cleaned_data)
    #     return cleaned_data

    # def save(self, *args, **kwargs):
    #     city = super().save(*args, **kwargs)
        
    #     for flights in self.available_flights:
    #         Flight.objects.filter(
    #             takeoff_place = takeoff_place,
    #             arrival_place = arrival_place,
    #             takeoff_time = date,
    #         )
    #     return city