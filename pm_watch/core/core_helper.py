import pyodbc

import re
import logging
import traceback

from pm_watch.core import date_core
from pm_watch.core.date_core import DATE_TOKEN_DICT
from pm_watch.helper.common import Constant, PathType, Setting, JobConfigError


def parse_file_name(file_name: str, offset_days: int = None, offset_hours: int = None) -> str:
    """parse an individual filename that contains '{<token>:<Date fmt>}'
    <Date fmt> is .NET based Date Format string. It will be converted to Python date format string
    if '<token>:' is missing, the default token is 'today'
    <Date fmt> such as 'YYYYMMDD' is always required to prevent confusion.
    """

    token: list[str] = re.findall(Constant.REGEX_FILE_NAME, file_name)

    if len(token) == 0:
        return file_name
    elif len(token) > 1:
        raise JobConfigError(f'file_name cannot have more than 1 variables: {file_name}')

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
    return file_name.replace('{' + token[0] + '}', parsed_date_str)


def validate_path_type(my_path: str) -> PathType:
    """validate and parse path type using regular expression"""

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
        raise JobConfigError(f'not a valid path: {my_path}')


def get_job_config_db(job_name: str) -> dict:
    server = 'rds-tps-dev-instance.cl8casj4jvue.us-east-1.rds.amazonaws.com,1433'
    database = 'tpsServices'
    username = 'tpstest'
    password = 'JB0t2oWpnRAf6pX'
    table = 'pm_watch_job_config'
    log = logging.getLogger()
    log.info(f'Getting job config from database {database}.dbo.{table} ... ')
    log.info(f'Opening SQL Server connection to {server} ... ')
    conn = pyodbc.connect(
        'Driver={SQL Server};Server='
        + server
        + ';Database='
        + database
        + ';UID='
        + username
        + ';PWD='
        + password
    )

    try:
        cursor = conn.cursor()
        cursor.execute(f'select top 1 * from dbo.{table} where job_name = ?', job_name)
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        if len(results) == 0:
            raise JobConfigError(f'job_name not found in table {database}.dbo.{table} : {job_name}')
        row = results[0]
        my_dict: dict = dict(zip(columns, row))
        # split file_name, copy_name, archive_name to list of file_names, so that pm_watch can handle multiple files
        if isinstance(my_dict['file_names'], str):
            my_dict['file_names'] = my_dict['file_names'].split(',')
        if isinstance(my_dict['copy_names'], str):
            my_dict['copy_names'] = my_dict['copy_names'].split(',')
        if isinstance(my_dict['archive_names'], str):
            my_dict['archive_names'] = my_dict['archive_names'].split(',')

    except Exception as ex:
        log.error(ex)
        if Setting.debug:
            log.error(traceback.format_exc())
        raise ex
    finally:
        conn.close()

    return my_dict
