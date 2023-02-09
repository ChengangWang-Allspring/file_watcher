import yaml

import argparse
import logging
import fnmatch
import time
import os

from pm_watch.helper.common import PathType, JobConfigError
from pm_watch.helper import file_helper
from pm_watch.core.config_core import ValidJobConfig
from pm_watch.stage import config_cache


def perform_watch() -> list:
    """File Watch primary while loop Logic"""

    log = logging.getLogger()
    log.info('<<< Watching file ... >>>')
    config = config_cache.config
    log.info(
        f'<<< Looking for file(s) ({config.effective_file_names}) from ({config.source_path}) >>>'
    )
    poll_attempt: int = 0
    while True:  # keep looking for until reaching max look_time
        poll_attempt += 1
        files = file_helper.get_files(config)  # get files from either local, UNC or S3 URI
        match = []
        if len(files) > 0:
            for filename in config.effective_file_names:
                log.debug(f'checking {filename}')
                match += fnmatch.filter(files, filename)  # use Python fnmatch to filter by filename
        # remove duplicate from the list
        if len(match) > 0:
            match = [*set(match)]  # remove posible duplicate by converting set

        if config.min_size is not None and config.min_size>0:
            pass  # check file size TODO

        if config.exclude_age is not None and config.exclude_age>0:
            pass # check file age TODO

        # TODO: check if file has stablized by where last modified date changes

        if len(match) >= config.file_count:
            log.info('=' * 80)
            log.info(
                f'Files Were Found In Location [ {len(match)} out of {config.file_count} ] -- {config.source_path}'
            )
            log.info(match)
            log.info('=' * 80)
            return match
        else:
            log.info(
                f'No file (or Not Enough files [ {len(match)} out of {config.file_count} ]) Were Found - Attempt {poll_attempt} out of {config.look_time} -- Sleeping for {config.sleep_time} Seconds --'
            )
            time.sleep(config.sleep_time)
            if poll_attempt >= config.look_time:
                log.error(
                    f'No File (or Not Enough Files [ 0 out of {config.file_count} ]) were Found in the requested amount of times.'
                )
                raise TimeoutError('Maximum polling times reached!')


def may_peform_copy(file_list: list):
    """copy files from effective source to effective target location"""

    config = config_cache.config

    if config.use_copy:
        log = logging.getLogger()
        log.info('<<< Copying file ... >>>')
        log.info(f'{"source_path"} : {config.source_path }')
        log.info(f'{"copy_path"} : {config.copy_path }')
        log.info(f'{"effective_file_names"} : {config.effective_file_names }')
        log.info(f'Files found by file_watch at source_path: {file_list}')
        file_helper.copy_files(config, file_list)
        log.info('=' * 80)


def may_perform_archive(file_list: list):
    """archive files from effective source to effective archive location"""

    config = config_cache.config

    if config.use_archive:
        log = logging.getLogger()
        log.info('<<< Archiving file ... >>>')
        log.info(f'{"source_path"} : {config.source_path }')
        log.info(f'{"archive_path"} : {config.archive_path }')
        log.info(f'{"effective_file_names"} : {config.effective_file_names }')
        log.info(f'Files found by file_watch at source_path: {file_list}')
        file_helper.archive_files(config, file_list)
        log.info('=' * 80)

    pass
