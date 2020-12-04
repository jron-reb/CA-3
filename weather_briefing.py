"""
    module provides up to date weather on a location chosen by the user, with an api key
    from the config.json file
"""

import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG, filename='sys.log')

def weather_api_key() -> str:
    """find personal api key from the config file config.json"""

    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Weather api located')
    return data['weather_briefing'][0]['weather_api']

def city_filter() -> list:
    """ find selected city to display weather of from config.json """
    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Cities for weather briefing located')
    return data['weather_briefing'][0]['city_name']

def get_weather() -> str:
    """
    Function prints details about weather in a given location

    Function asks user to input a city and then uses an api key to poll
    openweathermap.org for up to date weather.It then prints details about
    the weather such as the current air temperature and feels like temperature
    in celsius along with the weather description and then location
    """

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = weather_api_key()
    weather_reports = []
    for city in city_filter():
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        # print response object
        response = requests.get(complete_url)
        weather_dict = response.json()
        main = weather_dict["main"]
        current_air_temperature_celsius = round(main["temp"] -273.00, 2)
        feels_like_temperature_celsius = round(main["feels_like"] -273.00, 2)
        current_location = weather_dict["name"]
        weather = weather_dict["weather"]
        weather_description = weather[0]["description"]
        # print following values
        weather_reports.append(" The weather in " + str(current_location) +
        " is " + str(weather_description) + '.'
        " It is " + str(current_air_temperature_celsius) + " degrees Celsius" +
        " and feels like " + str(feels_like_temperature_celsius) + '. ')
    empty = ''
    logging.info('Weather briefing polled from api')
    return str(empty.join(weather_reports))

def weather_api_checker() -> int:
    """Function finds the HTTP response code when polling the api """

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = weather_api_key()
    for city in city_filter():
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        # print response object
        response = requests.get(complete_url)
    if response.status_code >= 400:
        logging.warning('HTTP GET request failed, response code is ' + str(response.status_code))
        return response.status_code
    logging.info('HTTP GET request succeeded')
    return response.status_code
