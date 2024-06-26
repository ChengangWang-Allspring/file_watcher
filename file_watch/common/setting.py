import logging
from typing import Optional
from datetime import date


class Setting:
    """store global settings, command arguments, etc"""

    debug: bool = False
    clear_readonly: bool = False
    db_profile: Optional[str] = None
    job_name: Optional[str] = None
    log_file_path: Optional[str] = None
    # job_config_path: str = None
    holidays_yes: list[date] = []
    holidays_no: list[date] = []

    @classmethod
    def print_log(cls) -> None:
        log = logging.getLogger()
        log.info('<< Global settings >>')
        log.info(f'{"debug"} : {Setting.debug }')
        log.info(f'{"clear_readonly"} : {Setting.clear_readonly }')
        log.info(f'{"db_profile"} : {Setting.db_profile }')
        log.info(f'{"job_name"} : {Setting.job_name }')
        log.info(f'{"log_file_path"} : {Setting.log_file_path }')
