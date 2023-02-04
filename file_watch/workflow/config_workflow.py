import yaml

import logging
import argparse

from file_watch.common import constants
from file_watch.common.valid_job_config import ValidJobConfig
from file_watch.common.job_config_factory import JobConfigFactory
from file_watch.common.enums import JOB_CONFIG_TYPE
from file_watch.common.settings import Settings
from file_watch.helpers import path_helper


def parse_args():
    '''
    File watch utility. Check README.md

    Example useage:
        python -m file_watch [-h] [-d] -run <job_name>
    required python version 3.11
    <job_name>.yml configuration file has to be in /conf folder.
    '''

    parser = argparse.ArgumentParser(description='File_watch utility for Autotys jobs')
    parser.add_argument('-run', dest='job_name', required=True, help='run job <job_name> ')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='force DEBUG log message')
    return parser.parse_args()


def config_logging(job_name: str):

    config = yaml.safe_load(constants.LOGGING_YML)
    Settings.log_file_path = path_helper.get_log_file_path(job_name)
    config['handlers']['file']['filename'] = Settings.log_file_path
    # overide logger's filename with <job_name> and date string embedded name
    logging.config.dictConfig(config)


def set_log_level(log, debug: bool) -> None:
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    log.setLevel(level)
    for handler in log.handlers:
        handler.setLevel(level)


def validate_job_config(job_name: str) -> ValidJobConfig:

    Settings.job_config_path = path_helper.get_jobs_yml_file_path(job_name)
    Settings.job_config_type = JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_YML
    config_dict: dict = JobConfigFactory.get_config_dict(job_name, JOB_CONFIG_TYPE.JOB_CONFIG_TYPE_YML)
    config = ValidJobConfig(**config_dict)
    return config
