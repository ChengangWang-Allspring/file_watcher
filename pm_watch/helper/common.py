import logging
from enum import Enum, auto
from pathlib import Path
from datetime import datetime


class Constant:
    """ constants that would never change """

    DATA_RELATIVE_PATH = 'data/'
    DATA_YML_RELATIVE_PATH = 'data/yml/'
    LOGS_RELATIVE_PATH = 'logs/'

    REGEX_S3_URI: str = r'^s3://([^/]+)/(.*?[^/]+/?)$'
    REGEX_UNC: str = r'^\\\\([a-zA-Z0-9_.$-]+\\[a-zA-Z0-9_.$-\\]+)$'
    REGEX_LOCAL: str = r'^[a-zA-Z]:\\(?:\w+\\?)*$'

    # file-name regex that accept one optional variable
    # that's wrapped in curly bracket {dt_token:dt_fmt}
    REGEX_FILE_NAME: str = r'\{([\s|\S][^\{\}]*)\}'

    # embeded logging.yml, 2 spaces indentation in this YML is critical
    LOGGING_YML = """
    version: 1
    disable_existing_loggers: true
    formatters:
      simple:
        format: '%(asctime)s - %(levelname)s - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        level: INFO
        formatter: simple
        stream: ext://sys.stdout
      file:
        class: logging.FileHandler
        level: DEBUG
        formatter: simple
        filename: <job-name_YYYYMMDD.log> 
    loggers:
      fileWatchLogger:
        level: DEBUG
        handlers: [console]
        propagate: yes
    root:
      level: DEBUG
      handlers: [console,file]
    """


class JobConfigError(Exception):
    """ custom job config error """
    pass


class JobConfigType(Enum):
    """ Job config types that are currently supported """

    YML_CONFIG = auto()
    CSV_CONFIG = auto()
    DB_CONFIG = auto()


class PathType(Enum):
    """ Path types that are currently supported """

    LOCAL_PATH = auto()
    UNC_PATH = auto()
    S3_PATH = auto()


class Setting:
    """ store global settings, command arguments, etc """

    # this is where we can switch to YML_Config or DB_Config (CSV_config TBD)
    # Effective JobConfigType
    job_config_type: JobConfigType = JobConfigType.DB_CONFIG

    debug: bool = False
    job_name: str = None
    log_file_path: str = None
    job_config_path: str = None

    @classmethod
    def print_log(cls):
        log = logging.getLogger()
        log.info('<< Settings >>')
        log.info(f'{"debug"} : {Setting.debug }')
        log.info(f'{"job_name"} : {Setting.job_name }')
        log.info(f'{"log_file_path"} : {Setting.log_file_path }')
        log.info(f'{"job_config_path"} : {Setting.job_config_path }')
        log.info(f'{"job_config_type"} : {Setting.job_config_type }')


def get_yml_file_path(job_name: str):
    """ get job yml config's absolute path  """

    # go up 2 levels relatively (to the root folder)
    path = Path(__file__).parent.parent
    path = path.joinpath(Constant.DATA_YML_RELATIVE_PATH).joinpath(
        f'{job_name}.yml')
    return path


def get_log_file_path(job_name: str):
    # get logs absolute path from this module's path
    path = Path(__file__).parent.parent
    str_date = datetime.today().strftime('%Y-%m-%d')
    path = path.joinpath(Constant.LOGS_RELATIVE_PATH).joinpath(
        f'{job_name}_{str_date}.log')
    return path
