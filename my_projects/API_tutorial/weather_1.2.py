#!/bin/python3

import requests
import json


api = 'bb4a02fc2c30f3faabcbafc1a7d96d71'


def geo_location():
    global lat, long
    city = input('Podaj nazwe miasta: ')
    city = city.capitalize()
    limit = 1
    geo_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}'.format(city, limit, api)
    resp = requests.get(geo_url)
    info = json.loads(resp.text)
    locate_dict = info[0]
    lat = locate_dict.get('lat')
    long = locate_dict.get('lon')


geo_location()

forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'. format(lat, long, api)

response = requests.get(forecast_url)
data = json.loads(response.text)


def get_today_forecast():
    current = data['list']
    current_dict = current[0]
    today = current_dict['main']
    print("Todays Forecast:")
    for elem in today:
        print(elem, today[elem])


get_today_forecast()


def get_five_day_forecast():
    global forecast_url
    forecast = data['list']
    forecast_dict = forecast[1]
    forecast_url = forecast_dict['main']
    print('\n', 'Forecast for next five day:')
    for element in forecast_url:
        print('daily averaged', element, forecast_url[element])


get_five_day_forecast()


def get_today_pollution_forecast():
    pol = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'.format(lat, long, api)

    respo = requests.get(pol)
    information = json.loads(respo.text)

    pollution = information['list']
    pollution_dict = pollution[0]
    aqi = pollution_dict['main']['aqi']
    components = pollution_dict['components']
    print('\n', 'Air Quality Index:', aqi, 'Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.')
    print('\n', 'Сoncentration of:')
    for component in components:
        print(component, components[component])


get_today_pollution_forecast()
