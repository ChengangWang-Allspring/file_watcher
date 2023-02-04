from abc import ABC, abstractmethod
from file_watch.common.enums import JOB_CONFIG_TYPE
from file_watch.helpers import config_helper


class BaseConfig(ABC):

    def __init__(self, job_name: str):
        self.job_name = job_name

    @abstractmethod
    def get_config_dict(self) -> dict:
        pass


class YamlJobConfig(BaseConfig):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        return config_helper.read_yaml_config(self.job_name)


class CsvJobConfig(BaseConfig):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from csv file passing job_name, translate some fields into dict')


class DbJobConfig(BaseConfig):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from database passing job_name, translate into dict')


class JobConfigFactory:

    # get job config dictionary based on type
    @staticmethod
    def get_config_dict(job_name: str, job_config_type: JOB_CONFIG_TYPE) -> dict:

        match job_config_type:
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_YML:
                config = YamlJobConfig(job_name)
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_CSV:
                config = CsvJobConfig(job_name)
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_DB:
                config = DbJobConfig(job_name)
            case _:
                return None
        return config.get_config_dict()
