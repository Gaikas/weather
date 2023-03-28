from django.shortcuts import render
import requests

def index(request):
    appid = "6f10b3c18f9c94b32a2be17ef126a439"
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=" + appid
    city = "Pinsk"
    res = requests.get(url.format(city)).json()
    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"],
    }
    context = {'info': city_info}
    return render(request, 'weather/index.html', context)
