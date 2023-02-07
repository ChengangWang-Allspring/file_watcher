import yaml

import argparse
import logging
import fnmatch
import time
import os

from pm_watch.helper.common import PathType, JobConfigError
from pm_watch.helper import file_helper
from pm_watch.core.config_core import ValidJobConfig
from pm_watch.stage import config_helper


def perform_watch() -> list:
    """ File Watch primary while loop Logic """

    log = logging.getLogger()
    log.info('<<< Watching file ... >>>')
    config = config_helper.config
    log.info(
        f"<<< Looking for file(s) ({config.effective_file_name}) from ({config.source_path}) >>>"
    )
    poll_attempt: int = 0
    while True:
        poll_attempt += 1
        files = get_files()
        match = []
        if len(files) > 0:
            for filename in config.effective_file_name:
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
                raise TimeoutError("Maximum polling times reached!")


def get_files() -> list:
    """ get filename list based on source path type"""

    config = config_helper.config
    log = logging.getLogger()
    if config.effective_source_path_type == PathType.S3_PATH:
        # list files from s3 bucket
        log.debug("Preparing to get files from s3 bucket ... ")
        bucket, prefix = file_helper.get_s3_bucket_prefix_by_uri(config.source_path)
        files = file_helper.get_files_on_s3(bucket, prefix)
        return files
    elif config.effective_source_path_type == PathType.LOCAL_PATH or config.effective_source_path_type == PathType.UNC_PATH:
        # list files on local path or UNC path
        log.debug("Preparing to get files from source path  ... ")
        return os.listdir(config.source_path)
    else:
        raise JobConfigError('effective_source_path_type is not derived')


def peform_copy(file_list: list):
    # copy files from effective source to effective target location

    pass


def perform_archive():
    # archive files from effective source to effective archive location

    pass
