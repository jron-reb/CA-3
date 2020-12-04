# CA-3
Smart alarm

Introduction:
This project is a smart alarm clock. It allows the user to set alarms that contain an update on the current covid-19
situation that is affecting everyone. It gives the option to include local weather and news briefings as well. When
an alarm is triggered it will announce this using text to speech. It will also automatically update the alarms every
day at 00:00 to find the latest covid-19 information, these notifications will expire after a set amount of time. This
information is polled from various sources in order to obtain up to date information.

Prerequisities:
The user must have an up to date python installed. As of creation of this alarm clock that would be python 3.9

The user requires a stable internet connection in order to run the alarm clock and poll the apis

The user requires a complete config file as attached with their own api keys

The news briefing module requires an api key that can be obtained at https://newsapi.org/.
  The news briefing module can be modified in the config file under news_briefing. The news sources and keywords
  that the api filters for as well as the country where the news come from can be altered as well as the maximum
  number of sources displayed. The user must also add their own api key before it is functional.
  Information about what sources and what countries is available at https://newsapi.org/v2/sources?apiKey=API_KEY.
  The link to the api is https://newsapi.org/

The weather briefing module requires an api key that can be obtained at https://newsapi.org/.
  The weather briefing module can be altered in the config under weather_briefing by the location that it provides.
  The link to the api is https://openweathermap.org/api, where more details can be found.

The covid_briefing module does not require an API key; however it requires the user to pip install uk-covid19
 or for a specific version of python -m pip install uk-covid19. The API is then set up to run but documentation
 about this can be found here https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/. It
 can be edited in the config file under "uk_covid19" for the location and the information it provides.

Notifications about the covid briefing will appear every day at 00:00. These can be removed manually or will be
removed automatically after 3 days. This can be edited in the config file under "notification_delay_before_removal".

The text to speech must be supported by installing pyttsx3. This can be done using pip install pyttsx 2.7
Python3.9 is not compatible with all drivers and therefore it is reccomended to install pytssx 2.7. However
other versions can be used.

GETTING STARTED
run main.py

open chrome (html template only compatible with chrome). Go to url 127.0.0.1:5000.
On the right a list of notifications will appear and on the a list of alarms appear. Currently both lists are empty.
Create an alarm by selecting the calendar. This is located in the bottom right of the button beneath the image.
Create a label for the alarm and check a tickbox if you would like to display a weather or news briefing. This will
then add an alarm on the left. The content will be updated and announced once the time that the alarm is set for at
is reached. The alarm can be removed using the x button in the top right hand corner. The timezone should not be an
issue as the server that is running is your device, which you will likely be using the alarm on. If this is not the
case then configure your device to be in the same timezone as the server you are running the alarm on.

LICENSE
MIT License

Copyright (c) [2020] [Jeroen Mijer]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

AUTHOR
Jeroen Mijer

VERSION
0.0.1

SOURCE
Github repo is """""add linnk """

ACKNOWLEDGEMENTS
Matt Collison for providing code throughout the different modules as well as the html template
