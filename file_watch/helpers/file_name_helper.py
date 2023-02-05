from file_watch.date_util import date_helper


def parse_file_name(file_name: str) -> str:

    token = 'TODAY'

    if token in file_name:
        return file_name.replace(token, date_helper.parse_date_token(token))
