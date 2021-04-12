from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import *

from .models import *

def index(request):
    query_results = Airport.objects.all()
    air_list = AirportChoiceField()

    context = {
        'query_results': query_results,
        'air_list': air_list,
    }
    print(air_list)
    return render(request,'homePage.html', context)