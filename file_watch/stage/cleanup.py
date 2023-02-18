from datetime import datetime
import logging

from file_watch.common.setting import Setting


def cleanup() -> None:
    log = logging.getLogger()
    now = datetime.now().strftime('%c')
    log.info(
        f'<<<<< File Watcher Job ({Setting.job_name}) -- Completed Successfully at ( {now} ) >>>>> '
    )
    log.info('EXIT 0')
