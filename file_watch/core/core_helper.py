import pyodbc

import re
import logging
import configparser
import logging
from pathlib import Path
from datetime import datetime

from file_watch.core import date_core
from file_watch.common.enum_const import Constant, PathType
from file_watch.common.setting import Setting


def parse_file_name(file_name: str, offset_days: int = 0, offset_hours: int = 0) -> str:
    """parse an individual filename that contains '{<token>:<Date fmt>}'
    <Date fmt> is .NET based Date Format string. It will be converted to Python date format string
    """

    token: list[str] = re.findall(Constant.REGEX_FILE_NAME, file_name)

    if len(token) == 0:
        return file_name
    elif len(token) > 1:
        raise ValueError(f'cannot have more than one date_token_fmt variables: {file_name}')

    date_token_fmt = token[0]
    log = logging.getLogger()
    log.info('-' * 80)
    log.info(f'parsing file_name: {file_name} ')
    log.info(f'date_token_fmt variable: {{{date_token_fmt}}}')

    date_token, date_fmt = date_core.split_date_token_fmt(date_token_fmt)

    # get date string by token and format
    parsed_date_str = date_core.parse_format_date(
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
        return PathType.NONE


def get_job_config_db(job_name: str) -> dict:
    """get job configuration from db profile"""

    log = logging.getLogger()

    # read database profile from data/db.ini
    config = configparser.ConfigParser()
    ini_path = (
        Path(__file__)
        .parent.parent.joinpath(f'{Constant.CONFIG_RELATIVE_PATH}/{Constant.DATABASE_INI}')
        .resolve()
    )
    config.read(ini_path)

    # get conn_string and table from database profile
    profile: str = 'default'
    if Setting.db_profile is not None and Setting.db_profile != '':
        profile = Setting.db_profile
    conn_string: str = ''
    if config.has_option(profile, 'conn_string'):
        conn_string = config.get(profile, 'conn_string')
    table: str = ''
    if config.has_option(profile, 'table'):
        table = config.get(profile, 'table')
    if conn_string == '' or table == '':
        raise ValueError(f'db_profile <{profile}>: conn_string or table is empty ')

    # use regular expression to match server and database
    reg_server_db = r'server=([\w.,-]*);[\S]*database=([\w]*);'
    matches = re.findall(reg_server_db, conn_string.lower())
    if len(matches[0]) != 2:
        raise ValueError(f'db_profile <{profile}>: errors in database conn_string in db.ini')
    server, database = matches[0]
    if server is None or server == '':
        raise ValueError(f'db_profile <{profile}>: db_server is empty in conn_string ')
    if database is None or database == '':
        raise ValueError(f'db_profile <{profile}>: database is empty in conn_string ')
    # if schema is not provided, assuming it is dbo
    if '.' not in table:
        table = f'dbo.{table}'

    log.info(f'Opening SQL Server connection: {server} ')
    log.info(f'Job config database: {database} ')
    log.info(f'Job config table: {table} ')

    conn = pyodbc.connect(conn_string)
    # get job configuration from datatbase table by job_name
    try:
        cursor = conn.cursor()
        cursor.execute(f'select top 1 * from {table} where job_name = ?', job_name)
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        if len(results) == 0:
            raise Exception(f'job_name not found in table {database}.{table} : {job_name}')
        row = results[0]
        my_dict: dict = dict(zip(columns, row))
        # split file_name, copy_name, archive_name to list of strings (required for ValidJobConfig)
        if isinstance(my_dict['file_names'], str):
            my_dict['file_names'] = my_dict['file_names'].split(',')
        if isinstance(my_dict['copy_names'], str):
            my_dict['copy_names'] = my_dict['copy_names'].split(',')
        if isinstance(my_dict['archive_names'], str):
            my_dict['archive_names'] = my_dict['archive_names'].split(',')

    except Exception as ex:
        raise ex
    finally:
        conn.close()

    return my_dict
