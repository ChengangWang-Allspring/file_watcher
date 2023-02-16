from datetime import datetime, date, timedelta
from typing import Dict, Callable
import holidays
import logging

from file_watch.helper.common import JobConfigError


DEFAULT_DATE_TOKEN = 'today'
DEFAULT_DATE_FORMAT = 'yyyyMMdd'

""" minus 20 hours offset for today_pm """
TODAY_PM_OFFSET_HOURS = -20

""" .NET Datetime format string to Python strftime() format string mapping """
_FORMAT_MAP = (
    ('yyyy', '%Y'),
    ('yyy', '%Y'),
    ('yy', '%y'),
    ('y', '%y'),
    ('MMMM', '%B'),
    ('MMM', '%b'),
    ('MM', '%m'),
    ('M', '%#m'),
    ('dddd', '%A'),
    ('ddd', '%a'),
    ('dd', '%d'),
    ('d', '%#d'),
    ('HH', '%H'),
    ('H', '%#H'),
    ('hh', '%I'),
    ('h', '%#I'),
    ('mm', '%M'),
    ('m', '%#M'),
    ('ss', '%S'),
    ('s', '%#S'),
    ('tt', '%p'),
    ('t', '%#p'),
    ('zzz', '%z'),
    ('zz', '%z'),
    ('z', '%#z'),
)


def cnv_csharp_date_fmt(in_fmt):
    """convert .NET date format to Python strftime date format"""

    ofmt = ''
    fmt = in_fmt
    while fmt:
        if fmt[0] == "'":
            # literal text enclosed in ''
            apos = fmt.find("'", 1)
            if apos == -1:
                # Input format is broken.
                apos = len(fmt)
            ofmt += fmt[1:apos].replace('%', '%%')
            fmt = fmt[apos + 1 :]
        elif fmt[0] == "\\":
            # One escaped literal character.
            # Note graceful behaviour when \ is the last character.
            ofmt += fmt[1:2].replace('%', '%%')
            fmt = fmt[2:]
        else:
            # This loop could be done with a regex "(yyyy)|(yyy)|etc".
            for intok, outtok in _FORMAT_MAP:
                if fmt.startswith(intok):
                    ofmt += outtok
                    fmt = fmt[len(intok) :]
                    break
            else:
                # Hmmmm, what does C# do here?
                # What do *you* want to do here?
                # I'll just emit one character as literal text
                # and carry on. Alternative: raise an exception.
                ofmt += fmt[0].replace('%', '%%')
                fmt = fmt[1:]
    return ofmt


def may_apply_offset(my_date: date, offset_days: int = None, offset_hours: int = None) -> date:
    """days/hours offset logic, negative offset means to move days/hours back"""

    if offset_days is not None and offset_days != 0:
        return my_date + timedelta(days=offset_days)

    if offset_hours is not None and offset_hours != 0:
        # convert from date to datetime
        dt: datetime = datetime.combineq(my_date, datetime.min.time())
        my_date = dt + timedelta(hours=offset_hours)
        return my_date.date()

    return my_date


def today(systime: datetime) -> date:
    """today"""

    return systime.date()


def today_pm(systime: datetime) -> date:
    """legacy token if hour before 20:00 use previous date"""

    return (systime + timedelta(hours=TODAY_PM_OFFSET_HOURS)).date()


def prev_weekday(systime: datetime) -> date:
    """last week day using weekday() function"""

    sysdate = systime.date()
    if sysdate.weekday() == 0:
        diff = 3
    elif sysdate.weekday() == 6:
        diff = 2
    else:
        diff = 1
    return sysdate - timedelta(days=diff)


def prev_day(systime: datetime) -> date:
    """previous day"""

    return datetime.now() + timedelta(days=-1)


def prev_bizday(systime: datetime) -> date:
    """previous business day excluding observed US holiday"""

    my_date = systime.date() + timedelta(days=-1)
    us_holidays = holidays.UnitedStates()
    while my_date in us_holidays or my_date.weekday() >= 5:
        my_date += timedelta(days=-1)
    return my_date


def last_bizday_of_last_month(systime: datetime) -> date:
    """last business day of previous month excluding observed US Holiday"""

    first = systime.date().replace(day=1)
    my_date = first - timedelta(days=1)
    us_holidays = holidays.UnitedStates()
    while my_date in us_holidays or my_date.weekday() >= 5:
        my_date += timedelta(days=-1)

    return my_date


def last_day_of_last_month(systime: datetime) -> date:
    """last day of last month"""

    my_date = systime.date().replace(day=1)
    return my_date + timedelta(days=-1)


def first_bizday_of_month(systime: datetime) -> date:
    """first business day of the current month"""

    my_date = systime.date().replace(day=1)
    us_holidays = holidays.UnitedStates()
    while my_date in us_holidays or my_date.weekday() >= 5:
        my_date += timedelta(days=1)
    return my_date


def first_day_of_month(systime: datetime) -> date:
    """first day of the current month"""

    return systime.date().replace(day=1)


# Date Token to func() mapping
date_token_dict: Dict[str, Callable[[datetime], date]] = {
    'today': today,
    'todayPm': today_pm,
    'prevWeekday': prev_weekday,  # previous work day
    'prevDay': prev_day,  # previous day
    'prevBizDay': prev_bizday,  # previous business day
    'lastBizDayOfLastMnth': last_bizday_of_last_month,  # last business day of last month
    'lastDayOfLastMnth': last_day_of_last_month,  # last day of last month
    'firsBizDayOfMnth': first_bizday_of_month,  # first business day of the current month
    'firsDayOfMnth': first_day_of_month,  # first day of the current month
}


def parse_date_token(
    token: str, dt_fmt: str, offset_days: int = None, offset_hours: int = None
) -> str:
    """parse date token and output formatted date string"""

    systime = datetime.now()
    log = logging.getLogger()
    log.info(f'system datetime: {systime.strftime("%c")}')
    log.info(f'date_token: {token}')
    log.info(f'date format: {dt_fmt}')
    if offset_days is not None and offset_days != 0:
        log.info(f'offset_days: {offset_days}')
    if offset_hours is not None and offset_hours != 0:
        log.info(f'offset_hours: {offset_hours}')

    ofmt = cnv_csharp_date_fmt(dt_fmt)
    my_date: date = None
    if token in date_token_dict.keys():
        my_date = date_token_dict[token](systime)

    if my_date is None:
        raise JobConfigError(f'date string transformation error')

    my_date = may_apply_offset(my_date, offset_days, offset_hours)
    date_string = my_date.strftime(ofmt)
    log.info(f'transformed date_string: {date_string}')

    return date_string
