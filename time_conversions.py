""" Module converts a given time into second """
import time
import logging

logging.basicConfig(level=logging.DEBUG, filename='sys.log')

def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds"""
    logging.info('minutes_to_seconds calculated')
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    logging.info('hours to minutes calculated')
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    """ Converts hours and minutes into seconds.

    Uses HH:MM where HH is a string of a 2 digit integer representing the hours.
    MM is a string of a 2 digit integer representing the minutes. This is taken and
    then converted into seconds
    """
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    logging.info('hhmm_to_seconds calculated')
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])

def hhmmss_to_seconds( hhmmss: str ) -> int:
    """ Converts hours and minutes and seconds into seconds.

    Uses HH:MM where HH is a string of a 2 digit integer representing the hours.
    MM is a string of a 2 digit integer representing the minutes. SS is a string of a 2 digit
    integer representing the second. This is taken and
    then converted into seconds
    """
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    logging.info('hhmmss_to_seconds calculated')
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])

def current_time_hhmm() -> str:
    """ Gives the current time in hours and minutes

    Where hh represents the hours and mm represents the minutes
    """
    logging.info('Current time calculated')
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)

if __name__ == '__main__':
    assert isinstance(minutes_to_seconds(10), int)
    assert minutes_to_seconds(10) == 600
    assert isinstance(hours_to_minutes(5), int)
    assert hours_to_minutes(5) == 300
    assert isinstance(hhmm_to_seconds('10:30'), int)
    assert (hhmm_to_seconds('10:30')) == 37800
    assert isinstance(hhmmss_to_seconds('10:30:30'), int)
    assert hhmmss_to_seconds('10:30:30') == 37830
    assert isinstance(current_time_hhmm(), str)
