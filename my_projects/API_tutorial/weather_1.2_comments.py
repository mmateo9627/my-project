#!/bin/python3

import requests
import json


api = 'bb4a02fc2c30f3faabcbafc1a7d96d71'


# geo_location(city) tak ma wygladac ta funkcja
def geo_location():
    # zadne global, 
    global lat, long
    # input do wyrzucenia
    city = input('Podaj nazwe miasta: ')
    city = city.capitalize()
    # to samo przypsanie do zmiennej zupelnie nie potrzebne
    limit = 1
    # tworzenie URL mozna przeniesc do osobnej funkcji construct_url() początek zawsze jest ten sam 
    geo_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}'.format(city, limit, api)
    resp = requests.get(geo_url)
    info = json.loads(resp.text)
    print(info)
    # 
    locate_dict = info[0]
    lat = locate_dict.get('lat')
    long = locate_dict.get('lon')
    # funkcja ma zwrócić w ostaniej linii return lat,longitude


# Funkcja ma miec postac geo_location(city='Katowice') jako parametr przyjmować nazwe miasta a nie pytac sie w inpucie
geo_location()

# to jak juz powinno isc na góre w kodzie a nie miedzy funkcjami
forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'. format(lat, long, api)

response = requests.get(forecast_url)
data = json.loads(response.text)

#
# def get_today_forecast():
#     current = data['list'][0]
#     # current dict to zla nazwa
#     # current_dict = current[0]
#     # print(current_dict)
#     weather = current['weather'][0]
#     description = weather['description']
#     today = current['main']
#     # print(today)
#     print(description)
#     # print("Todays Forecast:")
#     ##to samo zle nazwenictwo
#     for elem in today:
#         print(elem, today[elem])
#
# get_today_forecast()

#
# def get_five_day_forecast():
#     # nie ma byc zadnego globala
#     global forecast_url
#     forecast = data['list']
#     # forecast_dit to zla nazwa
#     forecast_dict = forecast[1]
#     forecast_url = forecast_dict['main']
#     print('\n', 'Forecast for next five day:')
#     # mowilem ze element to zła nazwa
#     for element in forecast_url:
#         print('daily averaged', element, forecast_url[element])
#
#
# get_five_day_forecast()
# #
#
# def get_today_pollution_forecast():
#     pol = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'.format(lat, long, api)
#
#     respo = requests.get(pol)
#     information = json.loads(respo.text)
#
#     pollution = information['list']
#     pollution_dict = pollution[0]
#     print (pollution_dict)
#     aqi = pollution_dict['main']['aqi']
#     components = pollution_dict['components']
#     print('\n',
#           'Air Quality Index:', {}, 'Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.'.format(aqi))
#     print('\n', 'Сoncentration of:')
#     for component in components:
#         print(component, components[component])
#
#
# get_today_pollution_forecast()
