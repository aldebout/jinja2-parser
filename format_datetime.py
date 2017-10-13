from babel.dates import format_datetime, get_timezone
from pytz import *
import datetime

def custom_format_datetime(value, format='date', tz='Europe/Paris', locale='fr_FR'):
    if format == 'date':
        format="dd/MM/yyyy"
    elif format == 'time':
        format="HH:mm"
    elif format == 'long_date':
        format="EEEE dd MMMM yyyy"
    return format_datetime(value, format, tzinfo=get_timezone(tz), locale=locale)

#jinja_env.filters['datetime'] = custom_format_datetime