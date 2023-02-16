import pyodbc

import re
import logging
import traceback
import configparser
import logging
from pathlib import Path
from datetime import datetime

from file_watch.core import date_parser
from file_watch.helper.common import Constant, PathType, Setting, JobConfigError, Setting


def parse_file_name(file_name: str, offset_days: int = None, offset_hours: int = None) -> str:
    """parse an individual filename that contains '{<token>:<Date fmt>}'
    <Date fmt> is .NET based Date Format string. It will be converted to Python date format string
    """

    token: list[str] = re.findall(Constant.REGEX_FILE_NAME, file_name)

    if len(token) == 0:
        return file_name
    elif len(token) > 1:
        raise JobConfigError(f'cannot have more than one date_token_fmt variables: {file_name}')

    date_token_fmt = token[0]
    log = logging.getLogger()
    log.info('-' * 80)
    log.info(f'parsing file_name: {file_name} ')
    log.info(f'date_token_fmt variable: {{{date_token_fmt}}}')

    date_token, date_fmt = date_parser.split_date_token_fmt(date_token_fmt)

    # get date string by token and format
    parsed_date_str = date_parser.parse_format_date(
        datetime.now(), date_token, date_fmt, offset_days, offset_hours
    )
    parsed_file_name = file_name.replace('{' + date_token_fmt + '}', parsed_date_str)
    log.info(f'effective_file_name: {parsed_file_name}')
    return parsed_file_name


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
    """get job configuration from db profile"""

    log = logging.getLogger()

    config = configparser.ConfigParser()
    ini_path = Path(__file__).parent.parent.joinpath(r'data\db.ini').resolve()
    config.read(ini_path)

    profile: str = 'default'
    if Setting.db_profile is not None and Setting.db_profile != '':
        profile = Setting.db_profile
    conn_string: str = None
    if config.has_option(profile, 'conn_string'):
        conn_string = config.get(profile, 'conn_string')
    table: str = None
    if config.has_option(profile, 'table'):
        table = config.get(profile, 'table')

    if conn_string is None or table is None:
        raise JobConfigError(f'db_profile <{profile}>: conn_string or table is empty ')
    reg_server_db = r'server=([\w.,-]*);[\S]*database=([\w]*);'
    matches = re.findall(reg_server_db, conn_string.lower())
    if len(matches[0]) != 2:
        raise JobConfigError(f'db_profile <{profile}>: errors in database conn_string in db.ini')
    server, database = matches[0]
    if server is None or server == '':
        raise JobConfigError(f'db_profile <{profile}>: db_server is empty in conn_string ')
    if database is None or database == '':
        raise JobConfigError(f'db_profile <{profile}>: database is empty in conn_string ')

    if '.' not in table:
        table = f'dbo.{table}'

    log.info(f'Opening SQL Server connection: {server} ')
    log.info(f'Job config database: {database} ')
    log.info(f'Job config table: {table} ')

    conn = pyodbc.connect(conn_string)

    try:
        cursor = conn.cursor()
        cursor.execute(f'select top 1 * from {table} where job_name = ?', job_name)
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        if len(results) == 0:
            raise JobConfigError(f'job_name not found in table {database}.{table} : {job_name}')
        row = results[0]
        my_dict: dict = dict(zip(columns, row))
        # split file_name, copy_name, archive_name to list of file_names, so that file_watch can handle multiple files
        if isinstance(my_dict['file_names'], str):
            my_dict['file_names'] = my_dict['file_names'].split(',')
        if isinstance(my_dict['copy_names'], str):
            my_dict['copy_names'] = my_dict['copy_names'].split(',')
        if isinstance(my_dict['archive_names'], str):
            my_dict['archive_names'] = my_dict['archive_names'].split(',')

    except Exception as ex:
        log.error(ex)
        log.debug(traceback.format_exc())
        raise ex
    finally:
        conn.close()

    return my_dict
