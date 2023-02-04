from enum import Enum


class PATH_TYPE(Enum):
    PATH_TYPE_LOCAL = 1
    PATH_TYPE__UNC = 2
    PATH_TYPE_S3 = 3


class JOB_CONFIG_TYPE(Enum):
    JOB_CONFIG_TYPE_YML = 1
    JOB_CONFIG_TYPE_CSV = 2
    JOB_CONFIG_TYPE_DB = 3
