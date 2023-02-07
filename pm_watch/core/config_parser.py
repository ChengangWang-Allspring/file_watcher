import re

from pm_watch.core import date_core
from pm_watch.core.date_core import DATE_TOKEN_DICT
from pm_watch.helper.common import Constant, PathType


def parse_file_name(file_name: str, offset_days: int = None, offset_hours: int = None) -> str:
    """ parse an individual filename that contains '{<token>:<Date fmt>}'
    <Date fmt> is .NET based Date Format string. It will be converted to Python date format string
    if '<token>:' is missing, the default token is 'today'
    <Date fmt> such as 'YYYYMMDD' is always required to prevent confusion.
    """

    token: list[str] = re.findall(Constant.REGEX_FILE_NAME, file_name)

    if len(token) == 0:
        return file_name
    elif len(token) > 1:
        raise SyntaxError(f'file_name cannot have more than 1 variables: {file_name}')

    if ':' in token[0]:
        date_token, date_fmt = token[0].split(':')
    else:
        if token[0] in DATE_TOKEN_DICT.keys():
            date_token = token[0]
            date_fmt = date_core.DEFAULT_DATE_FORMAT
        else:
            date_token = date_core.DEFAULT_DATE_TOKEN
            date_fmt = token[0]

    # get date string by token and format
    parsed_date_str = date_core.parse_date_token(date_token, date_fmt, offset_days, offset_hours)
    print(f'parsed_date_str: {parsed_date_str}')
    return file_name.replace('{'+token+'}', parsed_date_str)


def validate_path_type(my_path: str) -> PathType:
    """ validate and parse path type using regular expression """

    s3_path = re.findall(Constant.REGEX_S3_URI, my_path)
    unc_path = re.findall(Constant.REGEX_UNC, my_path)
    local_path = re.findall(Constant.REGEX_LOCAL, my_path)

    if s3_path and len(s3_path) > 0:
        return PathType.S3_PATH
    elif unc_path and len(unc_path) > 0:
        return PathType.UNC_PATH
    elif local_path and len(local_path) > 0:
        return PathType.LOCAL_PATH
    else:
        raise NotADirectoryError(f'not a valid path: {my_path}')
