from abc import ABC, abstractmethod

from pm_watch.helper.common import JobConfigType, JobConfigError
from pm_watch.helper import file_helper
from pm_watch.core import core_helper


class ConfigBase(ABC):
    """ abstract base config """

    def __init__(self, job_name: str):
        self.job_name = job_name

    @abstractmethod
    def get_config_dict(self) -> dict:
        pass


class YmlConfig(ConfigBase):
    """ Yml config """

    # overriding abstract method
    def get_config_dict(self) -> dict:
        # read yaml file into dictionary
        return file_helper.read_yml_config(self.job_name)


class CsvConfig(ConfigBase):
    """ CSV Config """

    # overriding abstract method
    def get_config_dict(self) -> dict:
        raise JobConfigError('CsvConfig not implemented in this release')


class DbConfig(ConfigBase):
    """ DB Config """

    # overriding abstract method
    def get_config_dict(self) -> dict:
        # get job config dictionary from datbase
        return core_helper.get_job_config_db(self.job_name)


class ConfigFactory:

    # get job config dictionary based on type
    @staticmethod
    def get_config_dict(job_name: str, job_config_type: JobConfigType) -> dict:

        match job_config_type:
            case JobConfigType.YML_CONFIG:
                config = YmlConfig(job_name)
            case JobConfigType.CSV_CONFIG:
                config = CsvConfig(job_name)
            case JobConfigType.DB_CONFIG:
                config = DbConfig(job_name)
            case _:
                return None
        return config.get_config_dict()
