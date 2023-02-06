from file_watch.core import date_core


def parse_file_name(file_name: str) -> str:

    token = 'TODAY'

    if token in file_name:
        return file_name.replace(token, date_core.parse_date_token(token))
