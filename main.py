""" This module is the main module used to run the alarm clock """

import logging
import datetime
import sched
import time
import json
import pyttsx3
from flask import request
from flask import Flask
from flask import render_template
from time_conversions import current_time_hhmm
from time_conversions import hhmm_to_seconds
from news_briefing import get_news
from weather_briefing import get_weather
from covid_briefing import get_covid



s = sched.scheduler(time.time, time.sleep)

engine = pyttsx3.init()

full_date = datetime.datetime.now()

logging.basicConfig(level=logging.DEBUG, filename='sys.log')
notifications = [{"title": 'alarm_item', "content": "whateva you want"}, {"title": '2', "content": "number 2"}, {"title": '3', "content": "number 3"}]
alarms = []
events = []
events_list = []

app = Flask(__name__)

def automatic_notifications_remover_appender():
    """ automatically adds notifications and removes notifications when called

    When called adds a notification containing the daily covid briefing.
    Checks if a notification has been in the notifications list for a predetermined
    time. If this time is reached the notification is removed

    """
    with open('config.json') as config_file:
        data = json.load(config_file)
    days_delayed_before_removal = data['notification_delay_before_removal']
    day_delay = datetime.timedelta(days = days_delayed_before_removal)
    today = str(full_date)
    notification_date = str(full_date - day_delay)
    notifications.append({"title": 'Daily covid briefing on ' + today[0:10], "content": get_covid()})
    logging.info('Notification added')
    for notification in notifications:
        if notification['title'] == 'Daily covid briefing on' + notification_date:
            notifications.remove(notification)
            (logging.info('Notification expired'))

def remove_alarm():
    "Removes alarms when the x button of an alarm is clicked"
    for event in events_list:
        if request.args.get("alarm_item") == event['title']:
            remove = events_list[events_list.index(event)]['content']
            if remove in s.queue:
                events_list.pop(events_list.index(event))
                s.cancel(remove)
    for alarm in alarms:
        if request.args.get("alarm_item") == alarm['title']:
            delete = alarms.index(alarm)
            alarms.pop(delete) #title and content cannot be the same but will almost never happen
    logging.info('Alarm removed')

def remove_notification():
    "Removes alarms when the x button of an alarm is clicked"
    for notification in notifications:
        for item in notification:
            if request.args.get("notif") == notification[item]:
                delete = notifications.index(notification)
                notifications.pop(delete) #title and content cannot be the same but will almost never happen
    logging.info('Notification removed')

def alarm_content() -> str:
    """ Determines alarm content and adds it to alarm.

    Checks whether the news and weather briefing tickboxes have been ticked.
    If they have been ticked it will poll the corresponding api and provide
    the corresponding information when the alarm goes off.
    If neither box has been ticked it returns just the get_covid api.

    """
    if request.args.get("weather") == 'weather' and request.args.get("news") == 'news':
        logging.info('Alarm set with information about covid, weather and news')
        return get_covid() + str(get_weather()) + str(get_news())
    if request.args.get("weather") == 'weather':
        logging.info('Alarm set with information about covid and weather')
        return get_covid() + str(get_weather())
    if request.args.get("news") == 'news':
        logging.info('Alarm set with information about covid and news')
        return get_covid() + str(get_news())
    if request.args.get("weather") != 'weather' and request.args.get("news") != 'news':
        logging.info('Alarm set with information about covid')
        return get_covid()

def set_alarm():
    """This function sets alarms

    It first checks whether the alarm has been set in the past. Which will cause it to log the alarm as in the past
    but will not append it.
    It then sets the alarm if it is set for today and if it is not it will add it to a list. Each day this list is checked
    and if the date on the alarm matches the date of the current day the alarm will be set for that day.
    When an alarm is set for today or added to a list to be set in the future, it will add an alarm on the left hand side of
    the interface with the title and the time that it will trigger.

    """
    alarm_time = request.args.get("alarm")
    alarm_hhmm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
    if full_date.year > int(alarm_time[0:4]) or full_date.month > int(alarm_time[5:7]) or full_date.day > int(alarm_time[8:10]):
        return logging.info('Alarm is in the past')
    if full_date.year == int(alarm_time[0:4]) and full_date.month == int(alarm_time[5:7]) and full_date.day == int(alarm_time[8:10]):
        if hhmm_to_seconds(alarm_hhmm) < hhmm_to_seconds(current_time_hhmm()):
            logging.info('Alarm is in the past')
            return render_template('index.html', title='Daily update', alarms=alarms, notifications=notifications, image='meme.jpg')
        delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())
        date = alarm_time[0:10]
        events.append({"date": date, "delay": delay, "event_title": request.args.get("two"), "time": alarm_hhmm})
        alarms.append({"title": request.args.get("two"), "content": 'Will be updated on announcement ( ' + alarm_time[0:10] + ' ' + alarm_time[12:] + ' )in order to provide relevant information'}) #changed from alarm content
        events_list.append({"title": request.args.get("two"), "content": s.enter(int(delay), 1, alarm_runner,(alarm_content(), request.args.get("two")))})
        logging.info('Alarm set for today at ' + alarm_time)
        return render_template('index.html', title='Daily update', alarms=alarms, notifications=notifications, image='meme.jpg')
    delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())
    date = alarm_time[0:10]
    events.append({"date": date, "delay": delay, "title": request.args.get("two"), "time": alarm_hhmm})
    alarms.append({"title": request.args.get("two"), "content": 'Will be updated on announcement ( ' + alarm_time[0:10] + ' ' + alarm_time[12:] + ' )in order to provide relevant information'})
    logging.info('Alarm set for ' + alarm_time + 'future date, will be scheduled on the date')
    return render_template('index.html', title='Daily update', alarms=alarms, notifications=notifications, image='meme.jpg')

def set_todays_alarms():
    """This function will set alarms due today

    Function takes from a list which stores alarms that were set for a day other than the day they were set.
    It check if the alarm is to be set on the current day. If it is it schedules it in the scheduler for the day,
    otherwise it does nothing.

    """
    for event in events:
        if full_date.year == int(event["date"][0:4]) and full_date.month == int(event["date"][5:7]) and full_date.day == int(event["date"][8:10]):
            events_list.append({"title": event["event_title"], "content": s.enter(int(event["delay"]), 1, alarm_runner,(alarm_content(), request.args.get("two")))})
            logging.info('Alarm set for today in ' + str(event["delay"]))
        else:
            continue

@app.route('/')
def controller():
    """ Function runs the alarm

    This function is what is called every time the page refreshes and is the homepage
    It holds the majority of the functionality of the alarm, with most larger modules running here.
    Function contains functions that schedules todays alarms and notifications. Sets alarms and removes
    notifications and alarms

    """
    alarm_time = request.args.get("alarm")
    s.run(blocking=False) #allows alarms to be scheduled without freezing the interface if a scheduled event is running
    logging.info('Page refreshed, running on controller')
    if current_time_hhmm() == '00:00': #set new alarms and notifications at midnight
        set_todays_alarms()
        automatic_notifications_remover_appender()
    if alarm_time: #if an alarm is scheduled
        set_alarm()
    if request.args.get("alarm_item"): #if an alarm is removed by the user (x in the corner clicked)
        remove_alarm()
    if request.args.get("notif"): #if a notification is removed by the user (x in the corner clicked)
        remove_notification()
    return render_template('index.html', title='Daily update', alarms=alarms, notifications=notifications, image='meme.jpg') #requires
    #renders the template (variables can be changed), requires render template and flask


@app.route('/index')
def index():
    "This is a page that returns when the page is refreshed and redirects to the controller"
    logging.info('index reached, controller returned')
    return controller()
    #for some reason it changes to index so this makes it like home screen

@app.route('/alarm_runner') #requires pyttsx3
def alarm_runner(announcement, title):
    """Function runs when alarm is scheduled

    The function first removes the previous label attached to an alarm saying when it will be announced.
    The function then adds a new alarm with updated information from the api polls.
    The function then uses pyttsx3 to announce the content of the alarm to the user.
    """
    for alarm in alarms: #in order to remove the alarm and add an updated one
        if title == alarm['title']:
            delete = alarms.index(alarm)
            alarms.pop(delete)
            logging.info('Alarm with no information removed')
    alarms.append({"title": title, "content": str(announcement)})
    logging.info('Alarm with up to date information added')
    try:
        engine.endLoop()
    except:
        pass
    engine.say(announcement)
    engine.runAndWait()
    logging.info('Alarm content announced')
    return render_template('index.html', title='Daily update', alarms=alarms, notifications=notifications, image='meme.jpg')

if __name__ == '__main__':
    logging.info('Application starting...')
    app.run()
