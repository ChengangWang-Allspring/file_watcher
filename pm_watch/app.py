import sys
import traceback
import logging
import logging.config
from datetime import datetime


from pm_watch.stage import prepare
from pm_watch.stage import action
from pm_watch.helper.common import Setting


def run():
    try:
        # parse arguments
        prepare.parse_args()

        # config logging
        prepare.config_logging()
        log = logging.getLogger()

        # initialize job config along with logger
        prepare.load_job_config()

        # must perform watch
        files = action.perform_watch()

        # may perform copy
        action.may_peform_copy(files)

        # may perform archive
        action.may_perform_archive(files)

    except Exception as ex:
        log.error('<<<<< Error caught in file_watcher main() >>>>>')
        log.error(type(ex).__name__)
        log.error(ex)
        if Setting.debug:
            log.error(traceback.format_exc())
        sys.exit(875)

    else:
        now = datetime.now().strftime('%c')
        log.info(
            f'<<<<< File Watcher Job ({Setting.job_name}) -- Completed Successfully at ( {now} ) >>>>> '
        )
        log.info('EXIT 0')

    finally:
        pass


if __name__ == '__main__':
    run()
