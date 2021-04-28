from .models import *
from .forms import *
from datetime import datetime, date
import datetime as dt

from rest_framework import serializers, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.db.models import Q 
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView


class CityListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homePage.html'

    def get(self, request):
        example_form = ExampleForm(request.GET)
        print(example_form)
        print('hey: {}'.format(example_form))
        return Response({'takeoff': example_form})

    def post(self, request):
        form = ExampleForm(request.POST)
        if form.is_valid():
            request.session['_old_post'] = request.POST
            if form.cleaned_data['my_date'] < datetime.now().date():
                form = ExampleForm(request.GET)
                return render(request, self.template_name, {'takeoff': form})
            else: 
                return HttpResponseRedirect('flights/')
        else:
            form = ExampleForm(request.GET)
        return render(request, self.template_name, {'form': form})


class SearchListView(generic.ListView):
    model = Flight
    template_name = 'search_results.html'
    context_object_name = 'flight_list'

    def get_queryset(self): # новый
        t_list = list()
        a_list = list()
        first_form_data = self.request.session.pop('_old_post',{})
        if first_form_data:
            print(first_form_data)
            takeoffs = Airport.objects.filter(
                Q(city_id__in=first_form_data['takeoff_place'])
            )
            arrivals = Airport.objects.filter(
                Q(city_id__in=first_form_data['arrival_place'])
            )
            print('Takeoff: {}'.format(takeoffs.values()))
            print('Arrival: {}'.format(arrivals.values()))
            for t in takeoffs:
                t_list.append(t.id)
            for a in arrivals:
                a_list.append(a.id)
            print(t_list)
            print(a_list)
            print(first_form_data['my_date'])
            my_date = first_form_data['my_date']
            print(datetime.now())
            date_time_obj = datetime.strptime(my_date, '%Y-%m-%d')
            print('Date: {}'.format(date_time_obj))
            print(t_list)
            print(a_list)
            flights = Flight.objects.filter(
                Q(takeoff_place_id__in=t_list) &
                Q(arrival_place_id__in=a_list) &
                Q(takeoff_time__date=datetime.date(date_time_obj))
            )
            print(flights)
            id_form = DetailForm(request.GET)
            print('ID for VIEW: {}'.forma(id_form))
            return flights.order_by('-takeoff_time').reverse()
        else:
            print(Airport.objects.all().values())
            print(Flight.objects.all().values())
            return Flight.objects.all().order_by('-takeoff_time').reverse()

    def get_context_data(self, **kwargs):
        takeoff_list = []
        arrival_list = []
        context = super(SearchListView, self).get_context_data(**kwargs)
        flights = context['flight_list'].values()
        context['airport_list'] = Airport.objects.all()
        context['city_list'] = City.objects.all()
        print('Flights: {}'.format(flights))
        print('Airports: {}'.format(context['airport_list'].values()))
        print('Cities: {}'.format(context['city_list'].values()))
        for fl in context['flight_list']:
        # for airs in context['airport_list']:
            # print('airport id: {}'.format(airs.id))
            for airs in context['airport_list']:
            # for cs in context['city_list']:
                # print('city id: {}'.format(cs.id))
                for cs in context['city_list']:
                # for fl in context['flight_list']:
                    # print('flight id: {}'.format(fl.id))
                    if (airs.id == fl.takeoff_place_id) and (cs.id == airs.city_id):
                        print('WHO?: {}'.format(fl.takeoff_place_id))
                        takeoff_list.append({
                            'id': fl.id,
                            'takeoff_id': fl.takeoff_place_id,
                            'name': airs.air_name,
                            'iata': airs.iata_code,
                            'city': cs.name,
                            'snum': fl.seats_number,
                            'tk_time': fl.takeoff_time,
                            'arr_time': fl.arrival_time, 
                        })
                    #     # Проблема в том, что в дальнейшем вылеты (id по вылетам) равны последнему элементу объекта класса Flight (arrival_place)
                    for tk in takeoff_list:
                        if (tk['id'] == fl.id) and (airs.id == fl.arrival_place_id) and (cs.id == airs.city_id):
                            print(fl.arrival_place_id)
                        # for tk in takeoff_list:
                            tk['arr_pl'] = fl.arrival_place_id
                            tk['arr_name'] = airs.air_name
                            tk['arr_iata'] = airs.iata_code
                            tk['arr_city'] = cs.name
        context['takeoffs'] = takeoff_list
        print(context['takeoffs'])
        return context

        def get(self):
            id_form = DetailForm(request.GET)
            print('ID for VIEW: {}'.forma(id_form))
            return Response({'id': id_form})

        def post(self):
            id_form = DetailForm(request.POST)
            print('ID for VIEW: {}'.forma(id_form))
            if id_form.is_valid():
                if ids_form:
                    request.session['flights_id'] = request.POST

            return render(request, 'polls/index.html', {})


class DetailFlightView(DetailView):
    model = Flight
    pk_url_kwarg = 'id'
    template_name = 'flight_detail.html'
    # queryset = Flight.objects.get(id=id)
    
    # def get_queryset(self):
    #     return Flight.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('no money')
        return redirect('no_edit', id=self.object.id)

    def get_context_data(self, **kwargs):
        context = super(DetailFlightView, self).get_context_data(**kwargs)
        context['flight'] = Flight.objects.get(id=id)
        return context

class AboutUsView(TemplateView):
    template_name = 'thanks.html'