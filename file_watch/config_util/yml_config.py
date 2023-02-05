from file_watch.config_util.config_base import ConfigBase
from file_watch.helpers import config_helper


class YmlConfig(ConfigBase):

    # overriding abstract method
    def get_config_dict(self) -> dict:
        # read yaml file into dictionary
        return config_helper.read_yml_config(self.job_name)
