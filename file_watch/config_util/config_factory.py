from file_watch.common.enums import JOB_CONFIG_TYPE
from file_watch.config_util.db_config import DbConfig
from file_watch.config_util.csv_config import CsvConfig
from file_watch.config_util.yml_config import YmlConfig


class ConfigFactory:

    # get job config dictionary based on type
    @staticmethod
    def get_config_dict(job_name: str, job_config_type: JOB_CONFIG_TYPE) -> dict:

        match job_config_type:
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_YML:
                config = YmlConfig(job_name)
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_CSV:
                config = CsvConfig(job_name)
            case JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_DB:
                config = DbConfig(job_name)
            case _:
                return None
        return config.get_config_dict()
