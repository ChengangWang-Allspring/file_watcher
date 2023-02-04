import yaml

import argparse
import logging
import fnmatch
import time
import os

from .static import *
from ..helpers import *
from ..helpers import *
from ..common.constants import *
from .static import *


def validate_job_config(job_yml_path: str) -> None:
    # initialize and validate JobConfig

    with open(job_yml_path, "r") as f:
        config_dict = yaml.safe_load(f)
    config = JobConfig(**config_dict)
    print(config.dict())


def config_logging(self) -> None:
    # validate log_path from <job_name>.yml, required for logger setup

    # check and set log_path from job config
    self.set_required_key("log_path")
    # check if log_path permission
    if not is_path_writable(self.log_path):
        raise JobConfigError(
            f"log_path is not correct or not writable: {self.log_path}"
        )

    # resolve absolute log_file_path
    date_str = datetime.today().strftime("%Y%m%d")
    path = Path(self.log_path).joinpath(f"{self.job_name}_{date_str}.log")
    self.LOG_FILE_PATH = path.resolve()

    # set up logger
    # with open(Path(__file__).parent.joinpath('logging.yml'), 'r') as f:
    # config = yaml.safe_load(f.read())
    config = yaml.safe_load(LOGGING_YML)
    print(f"configuring log_path in logger: {self.LOG_FILE_PATH}")
    # overide logger's filename using log_path
    config["handlers"]["file"]["filename"] = self.LOG_FILE_PATH
    logging.config.dictConfig(config)


def perform_watch() -> list:
    # File Watch - <while> loop Logic

    config = ConfigManager.get_config()
    log = logging.getLogger()
    log.info(
        f"<<< Looking for file(s) ({config.file_name}) from ({config.source_path}) >>>"
    )
    file_count: int = 0
    poll_attempt: int = 0
    while True:
        poll_attempt += 1
        files = get_files()
        match = []
        if len(files) > 0:
            for filename in config.file_name:
                log.debug(f"checking {filename}")
                match += fnmatch.filter(files, filename)
        # remove duplicate from the list
        if len(match) > 0:
            match = [*set(match)]

        if len(match) >= config.file_count:
            log.info(
                f"Files Were Found In Location [ {len(match)} out of {config.file_count} ] -- {config.source_path}"
            )
            log.info(match)
            return match
        else:
            log.info(
                f"No file (or Not Enough files [ {len(match)} out of {config.file_count} ]) Were Found - Attempt {poll_attempt} out of {config.look_time} -- Sleeping for {config.sleep_time} Seconds --"
            )
            time.sleep(config.sleep_time)
            if poll_attempt >= config.look_time:
                log.error(
                    f"No File (or Not Enough Files [ 0 out of {config.file_count} ]) were Found in the requested amount of times."
                )
                raise FileWatchTimeOutError("Maximum polling times reached!")


def get_files() -> list:
    # return filename list based on source type

    config = ConfigManager.get_config()
    log = logging.getLogger()
    if config.is_source_s3:
        # list files from s3 bucket
        log.debug("Preparing to get files from s3 bucket ... ")
        files = get_files_on_s3(config.source_s3_bucket,
                                config.source_s3_prefix)
        return files
    elif config.source_path:
        # list files on local path or UNC path
        log.debug("Preparing to get files from source path  ... ")
        return os.listdir(config.source_path)
    else:
        # this should be handled in JobConfig parse
        raise JobConfigError("Cannot resolve source.")


def peform_copy(file_list: list):
    # copy files from effective source to effective target location

    pass


def perform_archive():
    # archive files from effective source to effective archive location

    pass
