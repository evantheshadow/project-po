from .models import *
from .forms import *
from datetime import datetime, date

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


# def send_message(takeoff, arrival, date):


class CitySerializer(serializers.ModelSerializer):
    model = City
    fields = ("id", "name")


# class AirportSerializer(serializers.ModelSerializer):
#     model = Airport
#     fields = ("id", "iata_code", "air_name", "city")


class FlightSerializer(serializers.Serializer):
    fields = ("takeoff", "arrival", "date")

    takeoff = serializers.CharField()
    arrival = serializers.CharField()
    date = serializers.CharField()


class CityListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homePage.html'

    def get(self, request):
        example_form = ExampleForm(request.GET).as_p()
        print(example_form)
        print('hey: {}'.format(example_form))
        serializer = CitySerializer(get_cities(), many=True)
        return Response({'takeoff': example_form, 'serializer': serializer})

    def post(self, request):
        form = ExampleForm(request.POST)
        if form.is_valid():
            print('List of posted values: {}'.format(form))
            # serializer = FlightSerializer(form, many=True)
            # print('ser: {}'.format(serializer))
            request.session['_old_post'] = request.POST
            print('OLD POST SESSION: {}'.format(request.session['_old_post']))
            return HttpResponseRedirect('flights/')
        else:
            form = ExampleForm(request.GET)
        print('another one: {}, another two: {}'.format(form, self.template_name))
        return render(request, self.template_name, {'form': form})

# class AirportListView(APIView):
#     permission_classes = [AllowAny]
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'thanks.html'

#     def get(self, request):
#         airs = Airport.objects.all()
#         serializer = AirportSerializer(airs, many=True)
#         return Response({'airports': airs, 'serializer': serializer})


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
            flights = Flight.objects.filter(
                Q(takeoff_place_id__in=t_list) and
                Q(arrival_place_id__in=a_list)
            )
            print(flights.values())
            # cities = City.o
            # old_post = request.session.get('_old_post')
            # print('INDIAA:'.format(old_post))
            return flights
        else:
            print(Airport.objects.all().values())
            print(Flight.objects.all().values())
            return Flight.objects.all()

    def get_context_data(self, **kwargs):
        takeoff_list = []
        arrival_list = []
        # В первую очередь получаем базовую реализацию контекста
        context = super(SearchListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        # flights = context['flight_list'].values()
        context['airport_list'] = Airport.objects.all()
        context['city_list'] = City.objects.all()
        # print('Flights: {}'.format(flights))
        # print('Airports: {}'.format(context['airport_list'].values()))
        print('Cities: {}'.format(context['city_list'].values()))
        for airs in context['airport_list']:
            print('airport id: {}'.format(airs.id))
            for cs in context['city_list']:
        # for fl in context['flight_list']:
                print('city id: {}'.format(cs.id))
            # for airs in context['airport_list']:
            #     print('airport id: {}'.format(airs.id))
                # for cs in context['city_list']:
                for fl in context['flight_list']:
                    print('flight id: {}'.format(fl.id))
                    if (airs.id == fl.takeoff_place_id) and (cs.id == airs.city_id):
                        print(fl.takeoff_place)
                        takeoff_list.append({
                            'id': fl.takeoff_place_id,
                            'name': airs.air_name,
                            'iata': airs.iata_code,
                            'city': cs.name,
                            'snum': fl.seats_number,
                        })
                    for tk in takeoff_list:
                        if (airs.id == fl.arrival_place_id) and (cs.id == airs.city_id):
                            tk['arr_pl'] = fl.arrival_place_id
                    #     takeoff_list['arr_name'] = airs.air_name
                    #     takeoff_list['arr_iata'] = airs.iata_code
                    #     takeoff_list['arr_city'] = cs.name
                        # print(fl.arrival_place_id)
                        # print(airs.id)
                    # if (fl.arrival_place_id == airs.id):
                    #     print(airs.air_name)
                    #     takeoff_list['arr_pl'] = fl.arrival_place_id
                    #     takeoff_list['arr_name'] = airs.air_name
                    #     takeoff_list['arr_iata'] = airs.iata_code
                    #     takeoff_list['arr_city'] = cs.name
                        # fl.objects.annotate(tk_iata=airs.iata_code).filter(takeoff_place_id=airs.id)
                        # fl.takeoff_place_id = airs.iata_code
        # for fl in context['flight_list']:
        #     for tk in takeoff_list:
        #         for airs in context['airport_list']:
        #         # print('tk-id: {}'.format(tk['id']))
        #             for cs in context['city_list']:
        #                 if '{}, {}, {}'.format(fl.takeoff_place_id, fl.arrival_place_id, fl.takeoff_time) not in arrivals_set:
        #                 # if (airs.id == fl.arrival_place_id) and (tk['id'] == fl.takeoff_place_id) and (cs.id == airs.id):
        #                     tk['arr_pl'] = fl.arrival_place_id    
        #             # takeoff_list['arr_pl'] = fl.arrival_place_id
        #             #     takeoff_list['arr_name'] = airs.air_name
        #             #     takeoff_list['arr_iata'] = airs.iata_code
        #             #     takeoff_list['arr_city'] = cs.name
        #                     arrivals_set.add('{}, {}, {}'.format(fl.takeoff_place_id, fl.arrival_place_id, fl.takeoff_time))
        #                     print(arrivals_set)
        #                     print(fl.arrival_place_id)
                        
        # for tk in takeoff_list:
        #     for fl in context['flight_list']:  
        #         for airs in context['airport_list']:
        #             for cs in context['city_list']:  
        #                 if (fl.takeoff_place_id == tk['id']) and (fl.arrival_place_id == airs.id) and (cs.id == airs.id):
        #                     print(fl.arrival_place_id)
        #                     print(airs.air_name)
        #                 # for tk in takeoff_list:
        #                     tk['arr_pl'] = fl.arrival_place_id
        #                     tk['arr_name'] = airs.air_name
        #                     tk['arr_iata'] = airs.iata_code
        #                     tk['arr_city'] = cs.name
                            # arrival_list.append({
                            #     'id': fl.arrival_place_id,
                            #     'name': airs.air_name,
                            #     'iata': airs.iata_code,
                            #     'city': cs.name,
                            # })
                        # fl.objects.annotate(arr_iata=airs.iata_code).filter(arrival_place_id=airs.id)
                        # fl.arrival_place_id = airs.iata_code
        # context['airports'] = Airport.objects.filter(takeoff_place_id__in=context['airport_list'].values())
        context['takeoffs'] = takeoff_list
        context['arrivals'] = arrival_list
        print(context['takeoffs'])
        # print(context['flight_list'].values())
        return context


# class FlightListView(APIView):
#     permission_classes = [AllowAny]
#     renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'homePage.html'

#     def get(self, request):
#         response = Flight.objects.all()
#         take_set = set()
#         arr_set = set()
#         take_data = []
#         arr_data = []
#         for row in response:
#             if row.takeoff_place.air_name not in take_set:
#                 take_data.append({
#                     'id': row.takeoff_place.id,
#                     'name': row.takeoff_place.air_name,
#                     'iata_code': row.takeoff_place.iata_code,
#                 })
#                 take_set.add(row.takeoff_place.air_name)
#             if row.arrival_place.air_name not in arr_set:
#                 arr_data.append({
#                     'id': row.arrival_place.id,
#                     'name': row.arrival_place.air_name,
#                     'iata_code': row.arrival_place.iata_code
#                 })
#                 arr_set.add(row.arrival_place.air_name)
#             # row. 
#             print(row.takeoff_time)
#             row.date = row.takeoff_time.strftime('%d.%m.%Y')
#             # row.takeoff = row.takeoff_place.air_name
#             # row.arrival = row.arrival_place.air_name
#         serializer = FlightSerializer(response, many=True)
#         return Response({
#             'flights': response, 
#             'takeoffs': take_data, 
#             'arrivals': arr_data, 
#             'serializer': serializer
#         })