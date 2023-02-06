from datetime import datetime
from datetime import date

# .NET Datetime format string to Python strftime() format string mapping
_FORMAT_MAP = (
    ('yyyy', '%Y'), ('yyy', '%Y'), ('yy', '%y'), ('y', '%y'),
    ('MMMM', '%B'), ('MMM', '%b'), ('MM', '%m'), ('M', '%#m'),
    ('dddd', '%A'), ('ddd', '%a'), ('dd', '%d'), ('d', '%#d'),
    ('HH', '%H'), ('H', '%#H'), ('hh', '%I'), ('h', '%#I'),
    ('mm', '%M'), ('m', '%#M'), ('ss', '%S'), ('s', '%#S'),
    ('tt', '%p'), ('t', '%#p'), ('zzz', '%z'), ('zz', '%z'), ('z', '%#z')
)


def today() -> date:
    return date.today()


def parse_today_pm():
    pass


# Date Token to func() mapping
_DATE_DICT = {
    'today': today,
    'today_pm': parse_today_pm

}


def str_now() -> str:
    return datetime.now().strftime('%c')


def parse_date_token(token: str) -> str:

    if token == 'TODAY':
        return datetime.now().strftime('%Y%m%d')
    else:
        return None
