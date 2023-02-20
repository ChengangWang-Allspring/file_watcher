import logging
import fnmatch
import time

from datetime import datetime
from datetime import timedelta
from typing import List

from file_watch.common.enum_const import Constant
from file_watch.common import file_helper
from file_watch.stage import config_cache


def perform_watch() -> List[str]:
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
        # get 3 lists: files, modified_date_list and size_list from either local, UNC or S3 URI
        files, date_dict, size_dict = file_helper.get_files(config)
        match = []
        if len(files) > 0:
            for filename in config.effective_file_names:
                log.debug(f'checking {filename}')
                match += fnmatch.filter(files, filename)  # use Python fnmatch to filter by filename
        # remove duplicate from the list
        if len(match) > 0:
            match = [*set(match)]  # remove posible duplicate by converting set

        # check file size greater equal than min_size
        if config.min_size is not None and config.min_size > 0:
            for file in match:
                if size_dict[file] < config.min_size:
                    log.info(
                        f'1 file ({file}) skipped due to not reaching min_size {config.min_size}: actual file size {size_dict[file]}'
                    )
                    match.remove(file)

        # check file age (hours) is less than delta of file's last_modified
        if config.exclude_age is not None and config.exclude_age > 0:
            for file in match:
                delta: timedelta = datetime.now() - date_dict[file]
                if delta.total_seconds() > (config.exclude_age * 60 * 60):
                    log.info(
                        f'1 file ({file}) skipped due to too old. Last modified date: {date_dict[file]}'
                    )
                    match.remove(file)

        if len(match) >= config.file_count:
            log.info('=' * 80)
            log.info(
                f'Files Were Found In Location [ {len(match)} out of {config.file_count} ] -- {config.source_path}'
            )
            log.info('Waiting for files to stablize ... ')
            # check if file has stablized by where last modified date changes
            old_date_dict = {file: date_dict[file] for file in match}
            old_size_dict = {file: size_dict[file] for file in match}

            keep_waiting = True
            while keep_waiting:
                time.sleep(Constant.FILE_STABLIZE_INTERVAL)
                files, date_dict, size_dict = file_helper.get_files(config)
                keep_waiting = False
                for file in match:
                    if old_date_dict[file] != date_dict[file]:
                        old_date_dict[file] = date_dict[file]
                        keep_waiting = True
                    if old_size_dict[file] != size_dict[file]:
                        old_size_dict[file] = size_dict[file]
                        keep_waiting = True

            log.info('Files are stable (OK) ')
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


def may_peform_copy(file_list: List[str]) -> None:
    """copy files from effective source to effective target location"""

    config = config_cache.config

    if config.use_copy:
        log = logging.getLogger()
        log.info('<<< Copying file ... >>>')
        log.info(f'{"source_path"} : {config.source_path }')
        log.info(f'{"target_path"} : {config.target_path }')
        log.info(f'{"effective_file_names"} : {config.effective_file_names }')
        log.info(f'Files found by file_watch at source_path: {file_list}')
        file_helper.copy_files(config, file_list)
        log.info('=' * 80)


def may_perform_archive(file_list: list) -> None:
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
