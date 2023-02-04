from file_watch.common.valid_job_config import ValidJobConfig
from file_watch.common.enums import JOB_CONFIG_TYPE


class Settings:

    debug: bool = False
    job_name: str = None
    log_file_path: str = None
    job_config_path: str = None
    job_config_type: JOB_CONFIG_TYPE = None
    config_path: str = None
    config: ValidJobConfig = None
