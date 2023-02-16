#!/bin/python3
import sys
import requests
import json
import argparse


def main(args=None):

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(prog='weather-forecast')
    parser.add_argument('-c', '--city', type=str,
                        metavar='', required=True,
                        help='Name of the city for forecast to find, required.')
    parser.add_argument('-f', '--five', action="store_true",
                        required=False,
                        help='For five day forecast in the chosen city.')
    parser.add_argument('-p', '--pollution', action='store_true',
                        required=False,
                        help='For pollution forecast in the chosen city.')

    args = parser.parse_args()

    api = "bb4a02fc2c30f3faabcbafc1a7d96d71"

    lat, long = geo_location(city=args.city, api_key=api)

    forecast_url = create_url(_type="forecast", lat=lat, long=long, api=api)

    pollution_url = create_url(_type="air_pollution", lat=lat, long=long, api=api)

    response = requests.get(forecast_url)
    data = json.loads(response.text)

    get_today_forecast(data=data)
    if args.five is True:
        get_five_day_forecast(data=data)
    if args.pollution is True:
        get_today_pollution_forecast(pollution_air_url=pollution_url)
    
    return args


def geo_location(city: str, api_key: str):
    geo_url = (
        "http://api.openweathermap.org/geo/1.0/direct?q={}&limit={}&appid={}".format(
            city, 1, api_key
        )
    )
    resp = requests.get(geo_url)
    info = json.loads(resp.text)

    locate_dict: dict = info[0]

    lat = locate_dict.get("lat")
    long = locate_dict.get("lon")

    return lat, long


def create_url(_type: str, lat: str, long: str, api: str) -> str:
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/{}?lat={}&lon={}&appid={}".format(
            _type, lat, long, api
        )
    )

    return forecast_url


def get_today_forecast(data: dict) -> list:
    current = data["list"]
    todayForecast = current[0]
    components = todayForecast["main"]
    print("Todays Forecast:")
    for component in components:
        print(component, components[component])

    return components


def get_five_day_forecast(data: dict) -> list:
    forecast = data["list"]
    fiveDay = forecast[1]
    components = fiveDay["main"]
    print("\n", "Forecast for next five day:")
    for component in components:
        print("daily averaged", component, components[component])


def get_today_pollution_forecast(pollution_air_url: str) -> None:

    respo = requests.get(pollution_air_url)
    information = json.loads(respo.text)

    pollution = information['list']
    pollutionsForecast = pollution[0]
    aqi = pollutionsForecast["main"]["aqi"]
    components = pollutionsForecast["components"]
    print(
        "\n",
        "Air Quality Index:", aqi,
        "Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor."
    )
    print("\n", "Сoncentration of:")
    for component in components:
        print(component, components[component])


if __name__ == "__main__":

    main()

