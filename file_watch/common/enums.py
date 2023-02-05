from enum import Enum


class PATH_TYPE(Enum):
    PATH_TYPE_LOCAL = 1
    PATH_TYPE__UNC = 2
    PATH_TYPE_S3 = 3


class JOB_CONFIG_TYPE(Enum):
    JOB_CONFIG_TYPE_YML = 1
    JOB_CONFIG_TYPE_CSV = 2
    JOB_CONFIG_TYPE_DB = 3


class DATE_TOKEN(Enum):
    TODAY = 1
    TODAY_DELAYED = 2
    CURRENT_WEEK_DAY = 3  # current and most recent weekday
    LAST_WEEK_DAY = 4  # date of the previous weekday
    NEXT_WEEK_DAY = 5  # date of the next weekday
    LAST_WEEK_DAY_OF_CURRENT_MONTH = 3
