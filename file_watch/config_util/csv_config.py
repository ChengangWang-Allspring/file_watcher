from file_watch.config_util.config_base import ConfigBase
from file_watch.helpers import config_helper


class CsvConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from csv file passing job_name, translate some fields into dict')
