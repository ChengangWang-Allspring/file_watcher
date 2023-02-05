from file_watch.config_util.job_config import JobConfig
from file_watch.common.enums import JOB_CONFIG_TYPE


class Settings:

    CONFIG_RELATIVE_PATH = 'config/'
    CONFIG_YML_RELATIVE_PATH = 'config/jobs_yml/'
    LOGS_RELATIVE_PATH = 'logs/'

    debug: bool = False
    job_name: str = None
    log_file_path: str = None
    job_config_path: str = None
    job_config_type: JOB_CONFIG_TYPE = None
    config: JobConfig = None
