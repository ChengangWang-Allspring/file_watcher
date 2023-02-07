from datetime import datetime
from datetime import date
from datetime import timedelta
import holidays


DEFAULT_DATE_TOKEN = 'today'
DEFAULT_DATE_FORMAT = 'yyyyMMdd'

""" minus 20 hours offset for today_pm """
TODAY_PM_OFFSET_HOURS = -20

""" .NET Datetime format string to Python strftime() format string mapping """
_FORMAT_MAP = (
    ('yyyy', '%Y'), ('yyy', '%Y'), ('yy', '%y'), ('y', '%y'),
    ('MMMM', '%B'), ('MMM', '%b'), ('MM', '%m'), ('M', '%#m'),
    ('dddd', '%A'), ('ddd', '%a'), ('dd', '%d'), ('d', '%#d'),
    ('HH', '%H'), ('H', '%#H'), ('hh', '%I'), ('h', '%#I'),
    ('mm', '%M'), ('m', '%#M'), ('ss', '%S'), ('s', '%#S'),
    ('tt', '%p'), ('t', '%#p'), ('zzz', '%z'), ('zz', '%z'), ('z', '%#z')
)


def cnv_csharp_date_fmt(in_fmt):
    """ convert .NET date format to Python strftime date format """

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
            fmt = fmt[apos+1:]
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
                    fmt = fmt[len(intok):]
                    break
            else:
                # Hmmmm, what does C# do here?
                # What do *you* want to do here?
                # I'll just emit one character as literal text
                # and carry on. Alternative: raise an exception.
                ofmt += fmt[0].replace('%', '%%')
                fmt = fmt[1:]
    return ofmt


def offset(my_date: datetime, offset_days: int = None, offset_hours: int = None) -> datetime:
    """ apply days or hours offset logic.  Examples:
        offset_days = -1, offset 1 day back
        offset_hours = -20, offset 20 hours back
    """
    if offset_days != None and offset_days != 0:
        my_date += timedelta(days=offset_days)

    if offset_hours != None and offset_hours != 0:
        my_date += timedelta(hours=offset_hours)

    return my_date


def today(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ today  """
    return offset(date.today(), offset_days, offset_hours).strftime(fmt)


def today_pm(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ legacy token if hour before 20:00 use yesterday's date 
        default offset hours is -20. Recommends to leave offset_days and 
        offset_hours empty. 
    """
    if offset_hours == None or offset_hours == 0:
        my_date = datetime.now() + timedelta(hours=TODAY_PM_OFFSET_HOURS)
    else:
        my_date = datetime.now() + timedelta(hours=offset_hours)

    if offset_days != None and offset_days != 0:
        my_date += timedelta(days=offset_days)

    return my_date.strftime(fmt)


def lastwday(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ last week day using weekday() function """

    today = date.today()
    if today.weekday() == 0:
        diff = 3
    elif today.weekday() == 6:
        diff = 2
    else:
        diff = 1
    # subtracting diff
    my_date = today - timedelta(days=diff)
    return offset(my_date, offset_days, offset_hours).strftime(fmt)


def lastday(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ yesterday """

    my_date = datetime.now() + timedelta(days=-1)
    return offset(my_date, offset_days, offset_hours).strftime(fmt)


def lastbday(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ last business day excluding observed US holiday """

    today = date.today()
    # subtracting diff
    my_date = today + timedelta(days=-1)
    us_holidays = holidays.UnitedStates()
    while my_date in us_holidays or my_date.weekday() >= 5:
        my_date = my_date + timedelta(days=-1)
    return offset(my_date, offset_days, offset_hours).strftime(fmt)


def lbdom(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ last business day of previous month excluding observed US Holiday """

    today = date.today()
    first = today.replace(day=1)
    my_date = first - timedelta(days=1)
    us_holidays = holidays.UnitedStates()
    while my_date in us_holidays or my_date.weekday() >= 5:
        my_date = my_date + timedelta(days=-1)

    return offset(my_date, offset_days, offset_hours).strftime(fmt)


def ldom(fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ last day of previous month """

    today = date.today()
    first = today.replace(day=1)
    my_date = first - timedelta(days=1)
    return offset(my_date, offset_days, offset_hours).strftime(fmt)


# Date Token to func() mapping
DATE_TOKEN_DICT = {
    'today': today,
    'today_pm': today_pm,
    'lastwday': lastwday,  # last work day
    'lastday': lastday,
    'lastbday': lastbday,  # last business day
    'lbdom': lbdom,  # last business day of last month
    'ldom': ldom  # last day of last month
}


def str_now() -> str:
    """ print current date time string """

    return datetime.now().strftime('%c')


def parse_date_token(token: str, dt_fmt: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ parse date token and output formatted date string """

    ofmt = cnv_csharp_date_fmt(dt_fmt)
    if token in DATE_TOKEN_DICT.keys():
        return DATE_TOKEN_DICT[token](ofmt, offset_days, offset_hours)
    else:
        raise SyntaxError(f'date token or format error: {token}:{dt_fmt} ')
