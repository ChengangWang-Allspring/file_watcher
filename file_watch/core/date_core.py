from datetime import datetime, date, timedelta
from typing import Dict, Callable, Tuple, Optional
import holidays
import logging
import traceback


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


def cnv_csharp_date_fmt(in_fmt: str) -> str:
    """convert .NET date format to Python strftime date format"""

    ofmt: str = ''
    fmt: str = in_fmt
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


def datetime_offset(my_datetime: datetime, offset_days: int = 0, offset_hours: int = 0) -> datetime:
    """days/hours offset logic, negative offset means to move days/hours back"""

    my_datetime += timedelta(days=offset_days)
    my_datetime += timedelta(hours=offset_hours)
    return my_datetime


def today(systime: datetime) -> date:
    """today"""

    return systime.date()


def today_pm(systime: datetime) -> date:
    """legacy token if hour before 20:00 use previous date"""

    print(systime + timedelta(hours=TODAY_PM_OFFSET_HOURS))
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

    return systime.date() + timedelta(days=-1)


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


# Date Token to func() mapping, keys must be all lower cases
date_token_dict: Dict[str, Callable[[datetime], date]] = {
    'today': today,
    'todaypm': today_pm,
    'prevweekday': prev_weekday,  # previous work day
    'prevday': prev_day,  # previous day
    'prevbizday': prev_bizday,  # previous business day
    'lastbizdayoflastmnth': last_bizday_of_last_month,  # last business day of last month
    'lastdayoflastmnth': last_day_of_last_month,  # last day of last month
    'firsbizdayofmnth': first_bizday_of_month,  # first business day of the current month
    'firsdayofmnth': first_day_of_month,  # first day of the current month
}


def split_date_token_fmt(date_token_fmt: str) -> Tuple[str, str]:
    """split date variable into (token, format) tuple"""

    date_token = None
    date_fmt = None
    log = logging.getLogger()
    date_token_fmt = date_token_fmt.strip()
    if ':' in date_token_fmt:
        date_token, date_fmt = [x.strip() for x in date_token_fmt.split(':')]
        log.info(f'date_token: {{{date_token}}} ')
        log.info(f'date_format: {{{date_fmt}}}')
    else:
        if date_token_fmt.lower() in date_token_dict.keys():  # case insensitive
            date_token = date_token_fmt
            date_fmt = DEFAULT_DATE_FORMAT
            log = logging.getLogger()
            log.info(f'date_token: {{{date_token}}}')
            log.info(f'implicit default date_format: {{{DEFAULT_DATE_FORMAT}}} ')
        else:
            date_token = DEFAULT_DATE_TOKEN
            date_fmt = date_token_fmt
            log = logging.getLogger()
            log.info(f'implicit default date_token: {{{DEFAULT_DATE_TOKEN}}} ')
            log.info(f'date_format: {{{date_fmt}}}')

    return (date_token, date_fmt)


def parse_format_date(
    base_dt: datetime,
    token: str,
    dt_fmt: str,
    offset_days: Optional[int] = 0,
    offset_hours: Optional[int] = 0,
) -> str:
    """parse date token and output formatted date string"""

    log = logging.getLogger()
    log.info(f'system datetime: {base_dt.strftime("%c")}')

    offset_days = 0 if offset_days is None else offset_days
    offset_hours = 0 if offset_hours is None else offset_hours
    if offset_days != 0 or offset_hours != 0:
        log.info(f'applying offset_days = {offset_days}, offset_hours ={offset_hours}')
        base_dt = datetime_offset(base_dt, offset_days, offset_hours)
        log.info(f'offset system datetime: {base_dt.strftime("%c")}')

    ofmt = cnv_csharp_date_fmt(dt_fmt)
    my_date: Optional[date] = None
    if token.lower() in date_token_dict.keys():
        try:
            my_date = date_token_dict[token.lower()](base_dt)
        except Exception as e:
            log.error(f'date token transformation error: {e}')
            log.debug(traceback.format_exc())
            raise ValueError(f'date token transformation error: {e}')
    else:
        log.error(f'date token is not valid. {token}')
        log.error(f'valid token list: {date_token_dict.keys()}')
        raise ValueError(f'date token is not valid. {token}')

    if my_date is None:
        raise ValueError(f'date string transformation error')

    date_string = my_date.strftime(ofmt)
    log.info(f'transformed date_string: {date_string}')

    return date_string
