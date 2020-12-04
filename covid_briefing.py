"""
    module contains a function that polls the ukcovid api in order to find up to date
    information about coronavirus in the UK
    """
import json
import logging
from uk_covid19 import Cov19API
from requests import get

logging.basicConfig(level=logging.DEBUG, filename='sys.log')

def get_covid() -> str:
    """ Polls the ukcovid api in order to find up to date information about Covid-19 in the UK """
    with open('config.json') as config_file:
        data = json.load(config_file)

    filters = [
        'areaType=' + data["uk_covid19"][0]["area_type"],
        'areaName=' + data["uk_covid19"][0]["area_name"]
    ]

    structure = data["uk_covid19"][0]["structure"]

    api = Cov19API(filters=filters, structure=structure, latest_by = "newDeathsByDeathDate")

    covid_info = api.get_json()
    data = covid_info['data'][0]
    date = 'Date of information is ' + str(data['date']) + '.'
    new_cases = ' The number of new cases is ' + str(data['newCasesByPublishDate']) + '.'
    cum_cases = ' The number of cumulative cases is ' + str(data['cumCasesByPublishDate']) + '.'
    new_deaths = ' The number of new deaths is ' + str(data['newDeathsByDeathDate']) + '.'
    cum_deaths = ' The number of cumulative deaths is ' + str(data['cumDeathsByDeathDate']) + '. '
    return date + new_cases + cum_cases + new_deaths + cum_deaths

def covid_api_checker() -> int:
    """Function finds the HTTP response code when polling the api """
    endpoint = endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        'filters=areaType=nation;areaName=england&'
        'structure={"date":"date","newCases":"newCasesByPublishDate"}'
    )
    response = get(endpoint, timeout=10)

    if response.status_code >= 400:
        logging.warning('HTTP GET request failed, response code is ' + str(response.status_code))
        return response.status_code
    logging.info('HTTP GET request succeeded')
    return response.status_code
