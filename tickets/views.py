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
    widgets = {
                'birthdate': SelectDateWidget(attrs = {
                 },years = range(1920, 2017),),
             }

    takeoff = serializers.CharField()
    arrival = serializers.CharField()


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
        response = Flight.objects.all().distinct()
        for row in response: 
            row.date = row.date.strftime('%d.%m.%Y')
            row.takeoff = '{}. {}'.format(row.takeoff_place.id, row.takeoff_place.air_name)
            row.arrival = '{}. {}'.format(row.arrival_place.id, row.arrival_place.air_name)
        serializer = FlightSerializer(response, many=True)
        return Response({'flights': response, 'serializer': serializer})

    # def post(self, request):
    #     serializer = FlightSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)