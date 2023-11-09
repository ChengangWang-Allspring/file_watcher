import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from file_watch.common.setting import Setting
from file_watch.common import file_helper, s3_helper
from file_watch.common.enum_const import Constant, PathType, JobVerifyError
from file_watch.stage import config_cache


def may_verify(file_names: List[str]) -> bool:
    """verify if files exist on target_path or archive_path"""

    log = logging.getLogger()
    config = config_cache.config

    if config.files_decompress is not None and len(config.files_decompress)>0:
        # skip verifying files as the original compressed files are cleaned from target_path
        return True 

    if config.use_copy:
        log.info('Verifying files exist in target_path ... ')

    file_str = ','.join(file_names)
    if config.use_copy and config.effective_target_path_type == PathType.LOCAL_PATH:
        if not file_helper.verify_local_files(file_names, config.target_path):
            raise JobVerifyError(
                f'One of the files not found in target_path "{config.target_path}": {file_str}'
            )
    elif config.use_copy and config.effective_target_path_type == PathType.S3_PATH:
        if not s3_helper.verify_s3_files(file_names, config.target_path):
            raise JobVerifyError(
                f'One of the files not found in target_path "{config.target_path}": {file_str}'
            )

    if config.use_archive:
        log.info('Verifying files exist in archive_path ... ')
    if config.use_archive and config.effective_archive_path_type == PathType.LOCAL_PATH:
        if not file_helper.verify_local_files(file_names, config.archive_path):
            raise JobVerifyError(
                f'One of the files not found in archive_path "{config.archive_path}": {file_str}'
            )
    elif config.use_archive and config.effective_target_path_type == PathType.S3_PATH:
        if not s3_helper.verify_s3_files(file_names, config.archive_path):
            raise JobVerifyError(
                f'One of the files not found in archive_path "{config.archive_path}": {file_str}'
            )


def cleanup() -> None:
    """clean up resources"""

    log = logging.getLogger()
    # clean up aged logs
    log.debug('May clean up aged log files')
    try:
        log_path = Path(__file__).parent.parent.joinpath(Constant.LOGS_RELATIVE_PATH).resolve()
        obj = os.scandir(str(log_path))

        for entry in obj:  # iterate each DirEntry
            if entry.is_file():
                file_helper.may_clean_file(entry, ['*.log'], Constant.CLEANUP_LOG_AGE)

    except Exception as e:
        log.debug(e)

    now = datetime.now().strftime('%c')
    log.info(
        f'<<<<< File Watcher Job ({Setting.job_name}) -- Completed Successfully at ( {now} ) >>>>> '
    )
    log.info('EXIT 0')
