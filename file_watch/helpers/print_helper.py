import logging

from file_watch.config_util.job_config import JobConfig
from file_watch.common.settings import Settings


def print_settings():

    log = logging.getLogger()
    log.info('<< Settings >>')
    log.info(f'{"debug"} : {Settings.debug }')
    log.info(f'{"job_name"} : {Settings.job_name }')
    log.info(f'{"log_file_path"} : {Settings.log_file_path }')
    log.info(f'{"job_config_path"} : {Settings.job_config_path }')
    log.info(f'{"job_config_type"} : {Settings.job_config_type }')


def print_job_config(config: JobConfig):

    log = logging.getLogger()
    log.info('<< Job Config Variables >>')
    log.info(f'{"app_id"} : {config.app_id }')
    log.info(f'{"description"} : {config.description }')
    log.info(f'{"use_holiday"} : {config.use_holiday }')
    log.info(f'{"use_watch"} : {config.use_watch }')
    log.info(f'{"file_name"} : {config.file_name }')
    log.info(f'{"file_count"} : {config.file_count }')
    log.info(f'{"source_path"} : {config.source_path }')
    log.info(f'{"sleep_time"} : {config.sleep_time }')
    log.info(f'{"look_time"} : {config.look_time }')
    log.info(f'{"min_size"} : {config.min_size }')
    log.info(f'{"exclude_age"} : {config.exclude_age }')
    log.info(f'{"use_copy"} : {config.use_copy }')
    log.info(f'{"copy_name"} : {config.copy_name }')
    log.info(f'{"copy_path"} : {config.copy_path }')
    log.info(f'{"use_archive"} : {config.use_archive }')
    log.info(f'{"archive_name"} : {config.archive_name }')
    log.info(f'{"archive_path"} : {config.archive_path }')
    log.info('<< Resolved Variables >>')
    log.info(f'{"source_path_type"} : {config.source_path_type }')
    log.info(f'{"effective_file_name"} : {config.effective_file_name }')
