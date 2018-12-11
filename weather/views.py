from django.shortcuts import render
from .models import City
import requests
from .forms import CityForm
import datetime
from django.http import HttpResponse


# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d67e5071b35e20f461ee57b70f86c0ce'
   
    error = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        try:
            form.save()
        except:
            error = "City already exists"
    
    form = CityForm()

    cities = City.objects.all()
    
    ret = []
    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'main': r['weather'][0]['main'],
            'icon': r['weather'][0]['icon'],
        }

        ret.append(city_weather)

    context = {
        'cities_weather': ret,
        'form': form,
        'error': error
    }
    return render(request, 'weather/weather.html', context)


def detail(request, city):
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d67e5071b35e20f461ee57b70f86c0ce'
    r = requests.get(url.format(city)).json()

    context = {
        'city': r['name'],
        'icon': r['weather'][0]['icon'],
        'description': r['weather'][0]['description'],
        'temperature': r['main']['temp'],
        'pressure': r['main']['pressure'],
        'humidity': r['main']['humidity'],
        'temp_min': r['main']['temp_min'],
        'temp_max': r['main']['temp_max'],
        'wind_speed': r['wind']['speed']
    }
    return render(request, 'weather/detail.html', context)


def remove(request, city):
    City.objects.filter(name=city).delete()
    return index(request)

def convert_to_time(milsec):
    s = milsec / 1000.0
    time = datetime.datetime.fromtimestamp(s).strftime('%H:%M:%S')
    return time