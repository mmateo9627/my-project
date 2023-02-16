#!/bin/python3
import sys
import requests
import json
import argparse


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog='weather-forecast')
    required = parser.add_argument_group('Required')
    required.add_argument('-c', '--city', type=str,
                          metavar='', required=True,
                          help="Name of the city for forecast to find, required, for two-parts name ad '+' between.")
    optional = parser.add_argument_group('Optional')
    optional.add_argument('-f', '--five', action="store_true",
                          required=False,
                          help='For five day forecast in the chosen city.')
    optional.add_argument('-p', '--pollution', action='store_true',
                          required=False,
                          help='For pollution forecast in the chosen city.')

    args = parser.parse_args()

    api = 'bb4a02fc2c30f3faabcbafc1a7d96d71'

    temp = ['temp', 'feels_like', 'temp_min', 'temp_max']
    hpa = ['pressure', 'sea_level', 'grnd_level']

    try:
        lat, long = geo_location(city=args.city, api_key=api)

        forecast_url = create_url(_type='forecast', lat=lat, long=long, api=api)

        pollution_url = create_url(_type='air_pollution', lat=lat, long=long, api=api)

        response = requests.get(forecast_url)
        data = json.loads(response.text)

        get_today_forecast(data=data, temp=temp, hpa=hpa)
        if args.five is True:
            get_five_day_forecast(data=data, temp=temp, hpa=hpa)
        if args.pollution is True:
            get_today_pollution_forecast(pollution_air_url=pollution_url)
    except IndexError:
        print('City not found or You misspelled it')

    return args


def geo_location(city: str, api_key: str):

    geo_url = (
        'http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}'.format(
            city, 1, api_key
        )
    )

    resp = requests.get(geo_url)
    info = json.loads(resp.text)
    locate: dict = info[0]

    lat = locate.get('lat')
    long = locate.get('lon')
    return lat, long


def create_url(_type: str, lat: str, long: str, api: str) -> str:
    forecast_url = (
        'https://api.openweathermap.org/data/2.5/{}?lat={}&lon={}&appid={}&units=metric'.format(
            _type, lat, long, api
        )
    )

    return forecast_url


def get_today_forecast(data: dict, temp: list, hpa: list) -> list:
    current = data['list'][0]
    components = current['main']
    weather = current['weather'][0]
    where = data['city']
    name = where['name']
    description = weather['description']
    components.popitem()
    print('Today Forecast for {}:'. format(name), '\n', description)
    for component in components:
        if component in temp:
            print(component, components[component], '°C')
        elif component in hpa:
            print(component, components[component], 'hPa')
        else:
            print(component, components[component], '%')

    return components


def get_five_day_forecast(data: dict, temp: list, hpa: list) -> list:
    forecast = data['list'][1]
    components = forecast['main']
    weather = forecast['weather'][1]
    description = weather['description']
    components.popitem()
    print('\n', 'Forecast for next five day:', '\n', description)
    for component in components:
        if component in temp:
            print(component, components[component], '°C')
        elif component in hpa:
            print(component, components[component], 'hPa')
        else:
            print(component, components[component], '%')

def get_today_pollution_forecast(pollution_air_url: str) -> None:

    respo = requests.get(pollution_air_url)
    information = json.loads(respo.text)

    pollution = information['list'][0]
    aqi = pollution['main']['aqi']
    components = pollution['components']
    print(
        '\n',
        'Air Quality Index: {} Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.'.format(aqi)
    )
    print('\n', 'Сoncentration of:')
    for component in components:
        print(component, components[component], 'μg/m3')


if __name__ == '__main__':

    main()

