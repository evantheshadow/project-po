from .models import *
from .forms import *
from .functions import *

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


class CityListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homePage.html'

    def get(self, request):
        example_form = CityManagerForm(request.GET)
        print(example_form)
        return Response({'takeoff': example_form})

    def post(self, request):
        form = CityManagerForm(request.POST)
        if form.is_valid():
            request.session['_old_post'] = request.POST
            if form.cleaned_data['my_date'] < datetime.now().date():
                request.session['error_message'] = '{} уже наступило. Попробуйте ввести другую дату.'.format(form.cleaned_data['my_date'].strftime('%d.%m.%Y'))
                return HttpResponseRedirect('fl_error/')
            elif form.cleaned_data['takeoff_place'] == None and form.cleaned_data['arrival_place'] == None:
                request.session['error_message'] = 'Не выбран авиамаршрут. Выберите авиамаршрут, пожалуйста.'
                return HttpResponseRedirect('fl_error/')
            elif list(tk.id for tk in form.cleaned_data['takeoff_place'])[0] is list(tk.id for tk in form.cleaned_data['arrival_place'])[0]:
                request.session['error_message'] = 'Совпадают точки вылета и прилета. Выберите две разные точки вылета и прилета.'
                return HttpResponseRedirect('fl_error/')
            else: 
                return HttpResponseRedirect('flights/')
        else:
            form = CityManagerForm(request.GET)
        return render(request, self.template_name, {'form': form})


class SearchListView(generic.ListView):
    model = Flight
    template_name = 'search_results.html'
    context_object_name = 'flight_list'

    def get_queryset(self): 
        t_list = list()
        a_list = list()
        first_form_data = self.request.session.pop('_old_post',{})
        if first_form_data:
            takeoffs = Airport.objects.filter(
                Q(city_id__in=first_form_data['takeoff_place'])
            )
            arrivals = Airport.objects.filter(
                Q(city_id__in=first_form_data['arrival_place'])
            )
            for t in takeoffs:
                t_list.append(t.id)
            for a in arrivals:
                a_list.append(a.id)
            my_date = first_form_data['my_date']
            date_time_obj = datetime.strptime(my_date, '%Y-%m-%d')
            flights = Flight.objects.filter(
                Q(takeoff_place_id__in=t_list) &
                Q(arrival_place_id__in=a_list) &
                Q(takeoff_time__date=datetime.date(date_time_obj))
            )
            print(flights)
            return flights.order_by('-takeoff_time').reverse()
        else:
            return Flight.objects.all().order_by('-takeoff_time').reverse()

    def get_context_data(self, **kwargs):
        flight_api_list = []
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['airport_list'] = Airport.objects.all()
        context['city_list'] = City.objects.all()
        context['airline_team'] = AirlineTeam.objects.all()
        context['ticket_list'] = Ticket.objects.all()
        for fl in context['flight_list']:
            for airs in context['airport_list']:
                for cs in context['city_list']:
                    if (airs.id == fl.takeoff_place_id) and (cs.id == airs.city_id):
                        flight_api_list.append({
                            'id': fl.id,
                            'takeoff_id': fl.takeoff_place_id,
                            'name': airs.air_name,
                            'iata': airs.iata_code,
                            'city': cs.name,
                            'snum': fl.seats_number,
                            'tk_time': fl.takeoff_time,
                            'arr_time': fl.arrival_time,
                            'plane': fl.plane.name, 
                        })
                    for tk in flight_api_list:
                        if (tk['id'] == fl.id) and (airs.id == fl.arrival_place_id) and (cs.id == airs.city_id):
                            tk['arr_pl'] = fl.arrival_place_id
                            tk['arr_name'] = airs.air_name
                            tk['arr_iata'] = airs.iata_code
                            tk['arr_city'] = cs.name
                            tk['a_team'] = list(('{}: {} {} {} (Стаж: {} {})'.format(works.worker.position.name, works.worker.last_name, works.worker.first_name, works.worker.patro, works.worker.xp, xp_years(works.worker.xp))) for works in context['airline_team'] if (fl.id == works.flight_id))
                            tk['ticket'] = list(
                                ('{}: {}').format(ts.t_class, how_price_is_it(ts.price)) for ts in context['ticket_list'] if (fl.id == ts.flight_id)
                            )
        context['fapi_list'] = flight_api_list
        return context


class AboutUsView(TemplateView):
    template_name = 'thanks.html'

class ErrorView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'fl_error.html'

    def get(self, request):
        error = request.session.pop('error_message',{})
        return Response({'error': error})