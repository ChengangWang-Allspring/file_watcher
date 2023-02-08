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

        # perform watch
        files = action.perform_watch()

        action.peform_copy(files)

        action.perform_archive(files)

        """         if config.copy_file:
            log.info('<<< Copying file ... >>>')
            if len(file_list) > 0:
                peform_copy(file_list)
            else:
                raise FileWatchError('Unexpected empty file_list')

        if config.archive_file:
            log.info('<<< Archiving file ... >>>')
            perform_archive() """

    except Exception as ex:
        log.error('<<<<< Error caught in file_watcher main() >>>>>')
        log.error(ex)
        if Setting.debug:
            log.error(traceback.format_exc())
        sys.exit(875)

    else:
        now = datetime.now().strftime('%c')
        log.info(f'<<<<< File Watcher Job ({Setting.job_name}) -- Completed Successfully at ( {now} ) >>>>> ')
        log.info('EXIT 0')

    finally:
        pass


if __name__ == '__main__':
    run()
