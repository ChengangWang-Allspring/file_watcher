import yaml

import argparse
import logging

from pm_watch.helper.common import Setting, JobConfigType
from pm_watch.helper import constants
from pm_watch.helper import common
from pm_watch.core.config_factory import ConfigFactory
from pm_watch.core.config_core import ValidJobConfig
from pm_watch.helper import print_helper
from pm_watch.core import date_core


def parse_args():
    """
    File watch utility. Check README.md

    Example useage:
        python -m file_watch [-h] [-d] -run <job_name>
        required python version 3.11
    <job_name>.yml configuration file has to be in /conf folder.
    """

    parser = argparse.ArgumentParser(description='File_watch runner for Autotys jobs')
    parser.add_argument('job_name', help='job_name for file watcher to run ')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='force debug level log message')

    args = parser.parse_args()
    Setting.job_name = args.job_name
    Setting.debug = args.debug


def config_logging():
    """ configure logging """

    print('Configuring logger ...')
    config = yaml.safe_load(constants.LOGGING_YML)
    Setting.log_file_path = common.get_log_file_path(Setting.job_name)
    config['handlers']['file']['filename'] = Setting.log_file_path
    # overide logger's filename with <job_name> and date string embedded name
    logging.config.dictConfig(config)
    # set up log level
    log = logging.getLogger()
    level = logging.INFO
    if Setting.debug:
        level = logging.DEBUG
    print(f'Setting up log level to: {level}')
    log.setLevel(level)
    for handler in log.handlers:
        handler.setLevel(level)


def load_job_config():
    """ load job config, if validated, print all job variables """

    log = logging.getLogger()
    log.info('Parsing job configuration ... ')

    Setting.job_config_path = common.get_yml_file_path(Setting.job_name)
    Setting.job_config_type = JobConfigType.YML_CONFIG
    config_dict: dict = ConfigFactory.get_config_dict(Setting.job_name, JobConfigType.YML_CONFIG)
    config: ValidJobConfig = ValidJobConfig(**config_dict)
    Setting.config = config

    log.info(f'Initializing file watcher ...')
    print_helper.print_settings()

    # parse job config
    log.info('........................................................')
    log.info(
        f'<<<<< File Watcher Job ({Setting.job_name}) -- Started at ( {date_core.str_now()} ) >>>>> '
    )
    log.info('........................................................')
    print_helper.print_job_config(config)
