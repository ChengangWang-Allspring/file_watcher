import yaml

import argparse
import logging
from datetime import datetime
from typing import List

from file_watch.common import file_helper
from file_watch.common.enum_const import Constant, JobConfigType
from file_watch.common.setting import Setting
from file_watch.core.config_factory import ConfigFactory
from file_watch.core.config_core import ValidJobConfig
from file_watch.stage import config_cache


def parse_args(argv: List[str]) -> argparse.Namespace:
    """
    File watch utility. Check README.md

    Example useage:
        python -m file_watch [--db db_profile] [--debug]  <job_name>
        required python version 3.11
    <job_name>.yml configuration file has to be in /conf folder.
    """

    parser = argparse.ArgumentParser(description='File_watch runner for Autotys jobs')
    parser.add_argument('job_name', help='job_name for file watcher to run ')
    parser.add_argument(
        '--db',
        dest='db_profile',
        help='database profile that stores job configurations',
    )
    parser.add_argument(
        '--debug', dest='debug', action='store_true', help='force debug level log message'
    )
    return parser.parse_args(argv[1:])


def parse_args_to_settings(argv: List[str]) -> None:
    """parse command arguments into setting"""

    args = parse_args(argv)
    Setting.job_name = args.job_name
    Setting.debug = args.debug
    Setting.db_profile = args.db_profile


def config_logging() -> None:
    """configure logging"""

    print('Configuring logger ...')
    log_config = yaml.safe_load(Constant.LOGGING_YML)
    Setting.log_file_path = file_helper.get_log_file_path(Setting.job_name)
    log_config['handlers']['file']['filename'] = Setting.log_file_path
    # overide logger's filename with <job_name> and date string embedded name
    logging.config.dictConfig(log_config)
    # set up log level
    log = logging.getLogger()
    level = logging.INFO
    if Setting.debug:
        level = logging.DEBUG
    print(f'Setting up log level to: {level}')
    log.setLevel(level)
    for handler in log.handlers:
        handler.setLevel(level)


def load_job_config() -> None:
    """load job config, if validated, print all job variables"""

    log = logging.getLogger()
    log.info('Parsing job configuration ... ')

    config_dict: dict = ConfigFactory.get_config_dict(Setting.job_name, JobConfigType.DB_CONFIG)

    config = config_cache.config = ValidJobConfig(**config_dict)
    log.info(f'Initializing file watcher ...')

    Setting.print_log()

    log.info('=' * 80)
    now = datetime.now().strftime('%c')
    log.info(f'<<<<< File Watcher Job ({Setting.job_name}) -- Started at ( {now} ) >>>>> ')
    log.info('=' * 80)
    config.print_all_variables()
