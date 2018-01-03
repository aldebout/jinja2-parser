from babel.dates import format_datetime, get_timezone, format_timedelta
import pytz
from pytz import timezone
import datetime
from dateutil import parser
from base64 import b64encode
import json
import re

def filter_to_date(input, tzname='Europe/Paris'):
    """
        Parses a string into a datetime object, takes tzname as parameter.
        {{ "20171212T1212" |to_date }}
    """
    date = parser.parse(input)
    if date.tzinfo == None :
        return timezone(tzname).localize(date)
    return date

def filter_datetime(value, format='date', tz='Europe/Paris', locale='fr_FR'):
    """
        Pretty prints a datetime object according to parameters like format (in UTS-35 standard), tz and locale.
        {{ "20171212T1212" |to_date |datetime("EEEE dd-MM-yyyy 'à' HH'h'mm", "CET", locale='es_ES') }}
    """
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

def filter_timedelta(delta, granularity='minute', threshold=2, add_direction=False , format='short', locale='fr_FR'):
    """
        Pretty prints a timedelta object (difference between two datetimes).
    """
    return format_timedelta(delta, granularity=granularity, threshold=threshold, add_direction=add_direction, format=format, locale=locale)

def filter_b64encode(string):
    """
        Encodes an utf-8 string to base64
        {{ "Alexandre" |b64encode |safe }}
    """
    return b64encode(bytes(string, 'utf-8')).decode('UTF-8')

def filter_to_utf8(string):
    """
        Fixes some encoding problems that can be encountered when scraping the web.
        {{ "Nanterre-UniversitÃ©" |to_utf8 }}
    """
    return string.encode('LATIN-1').decode('UTF-8')

def filter_to_json( *args, **kwargs ):
    """
        Pretty prints à python object to valid JSON. Do not forget to use |safe.
        Wrapper for json.dumps, see official doc.
        {{ any_dict |to_json |safe }}
    """
    return json.dumps( *args, **kwargs)

def filter_from_json( *args, **kwargs ):
    """
        Loads a JSON string to a Python dict.
        Wrapper for json.loads, see official doc.
        {{ ("{\\"name\\":\\"Alexandre\\"}" |from_json).name }}
    """
    return json.loads( *args, **kwargs)

regex = re.compile(r'((?P<days>\d+?) days?, )?(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+?)')

def filter_to_timedelta(time_str):
    """
        Parses a timedelta string into a timedelta object.
        {{ "1 day, 17:02:31" |to_timedelta |timedelta }}
    """
    parts = regex.match(time_str)
    if not parts:
        raise ValueError('Couldn\'t find a valid timedelta in string')
    time_params = {}
    for (name, param) in parts.groupdict().items():
        if param:
            time_params[name] = int(param)
    return datetime.timedelta(**time_params)

def filter_regex_replace(string, regex, replace):
    """
        Searches and substitutes inside a string with a regex.
    """
    return re.sub(regex, replace, string)