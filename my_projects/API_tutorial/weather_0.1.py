#!/bin/python3

import requests
import json


api = "bb4a02fc2c30f3faabcbafc1a7d96d71"
lat = '50.258598'
long = '19.020420'

five_day = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'. format(lat, long, api)
pol = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'. format(lat, long, api)
units = 'Metric'

response = requests.get(five_day)
data = json.loads(response.text)

response2 = requests.get(pol)
data2 = json.loads(response2.text)


current = data['list']
curent_dict = current[0]
today = curent_dict['main']
print("Todays Forecast:")
for elem in today:
    print(elem, today[elem])

pollution  = data2['list']
polution_dict = pollution[0]
aqi = polution_dict['main']['aqi']
components = polution_dict['components']
print('\n','Air Quality Index:', aqi, 'Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.')
print('\n','Сoncentration of:')
for elem2 in components:
    print(elem2, components[elem2])


forecast = data['list']
forecast_dict = forecast[1]
five_day = forecast_dict['main']
print('\n','Forecast for next five day:')
for elem3 in five_day:
    print('daily averaged', elem3, five_day[elem3])