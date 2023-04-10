from django.shortcuts import render
import requests
from . models import City
from . forms import CityForm
from django.http import HttpResponse

def index(request):
    appid = "c818b06e8114d649adf450a0a9ca213c"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Такого города не существует!'
            else:
                err_msg = 'Такой город уже добавлен!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город добавлен успешно'
            message_class = 'is_success'



    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'wind': res['wind']['speed'],
            'icon': res['weather'][0]['icon'],
            }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
        'message': message,
        'message_class': message_class}

    return render(request, 'weather/index.html', context)

def about(request):
    return render(request, "weather/about.html")