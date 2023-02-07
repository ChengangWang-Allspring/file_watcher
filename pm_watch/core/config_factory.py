from abc import ABC, abstractmethod

from pm_watch.helper.common import JobConfigType
from pm_watch.helper import file_helper


class ConfigBase(ABC):

    def __init__(self, job_name: str):
        self.job_name = job_name

    @abstractmethod
    def get_config_dict(self) -> dict:
        pass


class YmlConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        # read yaml file into dictionary
        return file_helper.read_yml_config(self.job_name)


class CsvConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from csv file passing job_name, translate some fields into dict')


class DbConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from database passing job_name, translate into dict')


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
