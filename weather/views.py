from django.shortcuts import render
import requests
from dotenv import load_dotenv
load_dotenv()
import os

# Create your views here.
API_KEY = os.environ.get("API_KEY")


def index(request):
    if request.method == "POST":
        city = request.POST['city']
        params = {
            'q': city,
            'appid': API_KEY,
            'units':'metric'
        }
        
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        json_data = response.json()
        if json_data['cod'] == "404":
            print(json_data['cod'])
            data = {"error": f"'{city}' is not a valid city."}
            print("True")
        elif city:
            data = {
                "city": city.title(),
                'country_code': str(json_data['sys']['country']),
                'coordinates': str(json_data['coord']['lon']) + ', ' + str(json_data['coord']['lat']),
                'temp': str(json_data['main']['temp'])+'`C',
                'pressure': str(json_data['main']['pressure']),
                'humidity': str(json_data['main']['humidity']),
                'weather': str(json_data['weather'][0]['description']),
            }
        else:
            data = {"error": "Please provide a city."}
        
    else:
        data = ''
    return render(request, 'weather/index.html', {'data': data})