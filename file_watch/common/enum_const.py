from enum import Enum, auto


class Constant:
    """constants that would never change"""

    CONFIG_RELATIVE_PATH = 'config'
    LOGS_RELATIVE_PATH = 'logs'
    DATABASE_INI = 'db.ini'

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


class JobConfigType(Enum):
    """Job config types that are currently supported"""

    YML_CONFIG = auto()
    CSV_CONFIG = auto()
    DB_CONFIG = auto()
    NONE = auto()


class PathType(Enum):
    """Path types that are currently supported"""

    LOCAL_PATH = auto()
    UNC_PATH = auto()
    S3_PATH = auto()
    NONE = auto()
