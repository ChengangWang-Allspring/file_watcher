from file_watch.config_util.config_base import ConfigBase
from file_watch.helpers import config_helper


class DbConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        print(self.job_name)
        print('get dict from database passing job_name, translate into dict')
