from enum import Enum, auto
from pathlib import Path
from datetime import datetime

from pm_watch.core.config_core import ValidJobConfig


class Constant:
    """ constants that would never change """

    DATA_RELATIVE_PATH = 'data/'
    DATA_YML_RELATIVE_PATH = 'data/yml/'
    LOGS_RELATIVE_PATH = 'logs/'

    REGEX_S3_URI: str = '^s3://([^/]+)/(.*?[^/]+/?)$'
    REGEX_UNC: str = '^\\\\([a-zA-Z0-9_.$-]+\\[a-zA-Z0-9_.$-\\]+)$'
    REGEX_LOCAL: str = ''

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


class PathType(Enum):
    """ Path types that are currently supported """

    LOCAL_PATH = auto()
    UNC_PATH = auto()
    S3_PATH = auto()


class JobConfigType(Enum):
    """ Job config types that are currently supported """

    YML_CONFIG = auto()
    CSV_CONFIG = auto()
    DB_CONFIG = auto()


class Setting:
    """ global settings """

    debug: bool = False
    job_name: str = None
    log_file_path: str = None
    job_config_path: str = None
    job_config_type: JobConfigType = None
    config: ValidJobConfig = None


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
    path = path.joinpath(Setting.LOGS_RELATIVE_PATH).joinpath(
        f'{job_name}_{str_date}.log')
    return path
