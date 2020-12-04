"""
    Module provides up to date news from newsapi.org. The user can select
    news source(s) to always include along with keywords in the config.json
    file. The titles of these articles are then printed.
"""

import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG, filename='sys.log')

def news_api_key() -> str:
    """find personal api key from the config file config.json"""

    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('News api located')
    return data['news_briefing'][0]['news_api']

def source_filter() -> list:
    """ find selected news sources to display news from in news briefing from config.json """
    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Sources for news briefing located')
    return data['news_briefing'][0]['news_sources']

def keyword_filter() -> list:
    """ find key words in the title of news article to display in news briefing from config.json """
    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Keywords for news briefing located')
    return data['news_briefing'][0]['keywords']

def country_filter() -> str:
    """ find selected country to gather news from from config.json """
    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Countries for news briefing located')
    return data['news_briefing'][0]['country']

def max_news_sources () -> int:
    """ find maximum news sources that are displayed when an alarm is announced """
    with open('config.json') as config_file:
        data = json.load(config_file)
    logging.info('Number of maximum news sources for news briefing located')
    return data['news_briefing'][0]['maximum_sources'] + 1

def get_news() -> str:
    """Function prints titles of news articles

    Function uses an api key in order to poll newsapi.org for up to date
    articles from a selected news outlet containing the keywords selected
    by the user in the config file. The standard news outlet is BBC News
    and the keywords are ones related to coronavirus.
    """
    final_news_articles = []
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = news_api_key()
    for country in country_filter():
        location = country
        complete_url = base_url + "country=" + location + "&apiKey=" + api_key
        # print response object
        response = requests.get(complete_url)
        news_dict = response.json()
        articles = news_dict["articles"]
        main = news_dict['articles']
        final_news_articles.append('News from sources in ' + str.upper(country) + '. ')
        for article in articles:
            if len(final_news_articles) >= max_news_sources():
                empty = ''
                logging.info('Maximum number of articles recorded')
                return str(empty.join(final_news_articles))
            source_name = main[articles.index(article)]['source']['name']
            if source_name in source_filter():
                if article['title'] in final_news_articles:
                    continue
                final_news_articles.append(article['title'] + '. ')
        for article in articles:
            if len(final_news_articles) >= max_news_sources():
                empty = ''
                logging.info('Maximum number of articles recorded')
                return str(empty.join(final_news_articles))
            source_name = main[articles.index(article)]['source']['name']
            for keyword in keyword_filter():
                if keyword in article['title']:
                    if article['title'] in final_news_articles:
                        continue
                    final_news_articles.append(article['title'] + '. ')
        empty = ''
        logging.info('News briefing polled from api')
        return str(empty.join(final_news_articles))

def news_api_checker() -> int:
    """Function finds the HTTP response code when polling the api """

    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = news_api_key()
    for country in country_filter():
        location = country
        complete_url = base_url + "country=" + location + "&apiKey=" + api_key
        # print response object
        response = requests.get(complete_url)
    if response.status_code >= 400:
        logging.warning('HTTP GET request failed, response code is ' + str(response.status_code))
        return response.status_code
    logging.info('HTTP GET request succeeded')
    return response.status_code
