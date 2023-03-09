import pytz
from tzlocal import get_localzone

from datetime import datetime


def has_tz(my_date: datetime) -> bool:
    """Checking if a datetime object has timezone info"""

    return my_date.tzinfo is not None


def replace_tz_local(my_date: datetime) -> datetime:
    """force replacing a datetime's timezone with local timezone"""

    return my_date.replace(tzinfo=get_localzone())


def replace_tz_utc(my_date: datetime) -> datetime:
    """force replacing a datetime's timezone with UTC timezone"""

    return my_date.replace(tzinfo=pytz.UTC)


def remove_tz(my_date: datetime) -> datetime:
    """remove timezone from a datetime object"""

    return my_date.replace(tzinfo=None)


def utc_to_local(my_date: datetime) -> datetime:
    """convert from utc datetime to local datetime"""

    return my_date.astimezone(tz=get_localzone())


def local_to_utc(my_date: datetime) -> datetime:
    """convert from local datetime to utc datetime"""

    return my_date.astimezone(tz=pytz.UTC)
