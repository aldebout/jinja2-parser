from babel.dates import format_datetime, get_timezone, format_timedelta
import pytz
from pytz import timezone
import datetime
from dateutil import parser
from base64 import b64encode
import json

def filter_leetify(a, **kw):
    """Leetify text ('a' becomes '4', 'e' becomes '3', etc.)"""
    return a.replace('a','4').replace('e','3').replace('i','1').replace('o','0').replace('u','^')


def filter_datetime(value, format='date', tz='Europe/Paris', locale='fr_FR'):
    '''Pretty prints a datetime object according to parameters like format (in UTS-35 standard), tz and locale'''
    if format == 'date':
        format="dd/MM/yyyy"
    elif format == 'timeh':
        format="HH'h'mm"
    elif format == 'time':
        format="HH:mm"
    elif format == 'long_date':
        format="EEEE dd MMMM yyyy"
    elif format == 'daymonth':
        format="dd MMMM"
    return format_datetime(value, format, tzinfo=get_timezone(tz), locale=locale)

def filter_to_date(input, tzname='Europe/Paris'):
    '''Parses a string into a datetime object, takes tzname as parameter'''
    date = parser.parse(input)
    if date.tzinfo == None :
        return timezone(tzname).localize(date)
    return date

def filter_timedelta(delta, granularity='minute', threshold=2, add_direction=False , format='short', locale='fr_FR'):
    '''Pretty prints a timedelta object (difference between two datetimes). Takes parameters like granularity (minute, hour...), threshold (elasticity to granularity), format and locale.'''
    return format_timedelta(delta, granularity=granularity, threshold=threshold, add_direction=add_direction, format=format, locale=locale)

def filter_b64encode(string):
    '''Encodes an utf-8 string to base64'''
    return b64encode(bytes(string, 'utf-8')).decode('UTF-8')

filter_to_json = json.dumps

filter_from_json = json.loads

def filter_to_utf8(string):
    return string.encode('LATIN-1').decode('UTF-8')
