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
    fields = ("takeoff_place", "arrival_place", "date")


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
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        print(flights.values())
        return Response({'fly': flight, 'serializer': serializer})

    def post(self, request):
        serializer = FlightSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)