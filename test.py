from news_briefing import news_api_key
from news_briefing import source_filter
from news_briefing import keyword_filter
from news_briefing import country_filter
from news_briefing import max_news_sources
from news_briefing import get_news
from news_briefing import news_api_checker

from weather_briefing import weather_api_key
from weather_briefing import city_filter
from weather_briefing import get_weather
from weather_briefing import weather_api_checker

from covid_briefing import get_covid
from covid_briefing import covid_api_checker

if __name__ == '__main__':
    #test news_briefing
    assert isinstance(news_api_key(), str)
    assert isinstance(source_filter(), list)
    assert isinstance(keyword_filter(), list)
    assert isinstance(country_filter(), list)
    assert isinstance(max_news_sources(), int)
    assert isinstance(get_news(), str)
    assert news_api_checker() == 200

    #test weather_briefing
    assert isinstance(weather_api_key(), str)
    assert isinstance(city_filter(), list)
    assert isinstance(get_weather(), str)
    assert weather_api_checker() == 200

    #test covid_briefing
    assert isinstance(get_covid(), str)
    assert covid_api_checker() == 200
