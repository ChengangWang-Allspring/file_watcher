from enum import Enum, auto


class Constant:
    """constants that would never change"""

    FILE_STABLIZE_INTERVAL: int = 2  # wait interval in seconds for file stabilize

    CONFIG_RELATIVE_PATH = 'config'
    LOGS_RELATIVE_PATH = 'logs'
    DATABASE_INI = 'db.ini'
    CLEANUP_LOG_AGE = 2  # log aged in ?? days to be cleaned up

    REGEX_S3_URI: str = r'^s3://([^/]+)/(.*?[^/]+/?)$'
    REGEX_UNC: str = r'^\\\\([a-zA-Z0-9_.$-]+\\[a-zA-Z0-9_.$-\\]+)$'
    REGEX_LOCAL: str = r'^[a-zA-Z]:\\(?:[\w-]+\\?)*$'

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

    # Ascii art
    ASCII_ART_LOGO = r"""
        __ _ _                      _       _     
       / _(_) | ___  __      ____ _| |_ ___| |__  
      | |_| | |/ _ \ \ \ /\ / / _` | __/ __| '_ \ 
      |  _| | |  __/  \ V  V / (_| | || (__| | | |
      |_| |_|_|\___|   \_/\_/ \__,_|\__\___|_| |_|
    """

    ASCII_ART_SUCESS = r"""
       ___ _   _  ___ ___ ___  ___ ___ 
      / __| | | |/ __/ __/ _ \/ __/ __|
      \__ \ |_| | (_| (_|  __/\__ \__ \
      |___/\__,_|\___\___\___||___/___/
    """

    ASCII_ART_ERROR = r"""
       ___ _ __ _ __ ___  _ __ 
      / _ \ '__| '__/ _ \| '__|
     |  __/ |  | | | (_) | |   
      \___|_|  |_|  \___/|_|   
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


class JobVerifyError(Exception):
    """custom exception when verification fails"""

    pass
