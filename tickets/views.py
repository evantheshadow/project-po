# from django.http import HttpResponse
# from django.template import loader
# from django.shortcuts import render
# from django.views.generic.edit import CreateView
# from .forms import *

# from .models import *

# def index(request):
#     # query_results = Airport.objects.all()
#     # air_list = AirportChoiceField()

#     # context = {
#     #     'query_results': query_results,
#     #     'air_list': air_list,
#     # }
#     # print(air_list)
#     # return render(request,'homePage.html', context)

from .models import *
from rest_framework import serializers, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404


class AirportSerializer(serializers.ModelSerializer):
    model = Airport
    fields = ("id", "iata_code", "air_name", "city")


class FlightSerializer(serializers.ModelSerializer):
    model = Flight 
    fields = ("takeoff", "arrival", "date")
#     widgets = {
#                 'birthdate': SelectDateWidget(attrs = {
#                  },years = range(1920, 2017),),
#              }

    date = serializers.CharField()
    arrival = serializers.CharField()
    takeoff = serializers.CharField()


class AirportListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homePage.html'

    def get(self, request):
        airs = Airport.objects.all()
        serializer = AirportSerializer(airs, many=True)
        return Response({'airports': airs, 'serializer': serializer})


class FlightListView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'homePage.html'

    def get(self, request):
        response = Flight.objects.all()
        take_set = set()
        arr_set = set()
        take_data = []
        arr_data = []
        for row in response:
            if row.takeoff_place.air_name not in take_set:
                take_data.append({
                    'id': row.takeoff_place.id,
                    'name': row.takeoff_place.air_name,
                    'iata_code': row.takeoff_place.iata_code,
                })
                take_set.add(row.takeoff_place.air_name)
            if row.arrival_place.air_name not in arr_set:
                arr_data.append({
                    'id': row.arrival_place.id,
                    'name': row.arrival_place.air_name,
                    'iata_code': row.arrival_place.iata_code
                })
                arr_set.add(row.arrival_place.air_name)
            # row. 
            print(row.takeoff_time)
            row.date = row.takeoff_time.strftime('%d.%m.%Y')
            # row.takeoff = row.takeoff_place.air_name
            # row.arrival = row.arrival_place.air_name
        serializer = FlightSerializer(response, many=True)
        return Response({
            'flights': response, 
            'takeoffs': take_data, 
            'arrivals': arr_data, 
            'serializer': serializer
        })