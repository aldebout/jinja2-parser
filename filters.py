from babel.dates import format_datetime, get_timezone, format_timedelta
import pytz
import datetime
from dateutil import parser

def filter_leetify(a, **kw):
    """Leetify text ('a' becomes '4', 'e' becomes '3', etc.)"""
    return a.replace('a','4').replace('e','3').replace('i','1').replace('o','0').replace('u','^')


def filter_datetime(value, format='date', tz='Europe/Paris', locale='fr_FR'):
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

def filter_to_date(input):
    return parser.parse(input)

def filter_timedelta(delta, granularity='second', threshold=2, add_direction=True, format='short', locale='fr_FR'):
    return format_timedelta(delta, granularity, threshold, add_direction, format, locale)