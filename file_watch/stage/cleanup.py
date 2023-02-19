import os
import logging
from datetime import datetime
from pathlib import Path

from file_watch.common.setting import Setting
from file_watch.common.file_helper import may_clean_file
from file_watch.common.enum_const import Constant


def cleanup() -> None:
    log = logging.getLogger()

    # clean up aged logs
    log.debug('May clean up aged log files')
    try:
        log_path = Path(__file__).parent.parent.joinpath(Constant.LOGS_RELATIVE_PATH).resolve()
        obj = os.scandir(str(log_path))

        for entry in obj:  # iterate each DirEntry
            if entry.is_file():
                may_clean_file(entry, ['*.log'], Constant.CLEANUP_LOG_AGE)

    except Exception as e:
        log.debug(e)

    now = datetime.now().strftime('%c')
    log.info(
        f'<<<<< File Watcher Job ({Setting.job_name}) -- Completed Successfully at ( {now} ) >>>>> '
    )
    log.info('EXIT 0')
