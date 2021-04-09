from django.shortcuts import render
from django.urls import path

def index(request):
    return render(request, 'homePage.html')
    # return HttpResponse("Приветствую, пока данная версия является тестовой для программного модуля 'Авиакасса'.")