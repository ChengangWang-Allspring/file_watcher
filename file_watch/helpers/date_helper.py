from datetime import datetime


def str_now() -> str:
    return datetime.now().strftime('%c')


def parse_date_token(token: str) -> str:

    if token == 'TODAY':
        return datetime.now().strftime('%Y%m%d')
    else:
        return None
