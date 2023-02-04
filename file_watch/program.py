import sys
import traceback
import logging
import logging.config
from pathlib import Path

from file_watch.workflow import config_workflow
from file_watch.common.valid_job_config import ValidJobConfig
from file_watch.common.settings import Settings
from file_watch.helpers import date_helper
from file_watch.helpers import print_helper


def main():

    try:
        # parse arguments
        args = config_workflow.parse_args()
        Settings.debug = args.debug
        Settings.job_name = args.job_name

        # config logging
        print('Configuring logger ...')
        config_workflow.config_logging(args.job_name)
        log = logging.getLogger()
        config_workflow.set_log_level(log, Settings.debug)

        # initialize job config along with logger
        log.info('Parsing job configuration ... ')
        config: ValidJobConfig = config_workflow.validate_job_config(args.job_name)
        Settings.config = config

        log.info(f'Initializing file watcher ...')
        print_helper.print_settings()

        # parse job config
        log.info('........................................................')
        log.info(
            f'<<<<< File Watcher Job ({Settings.job_name}) -- Started at ( {date_helper.str_now()} ) >>>>> '
        )
        log.info('........................................................')
        print_helper.print_job_config(config)

        sys.exit(0)

        file_list = []
        if config.watch_file:
            log.info('<<< Watching file ... >>>')
            file_list = perform_watch()

        if config.copy_file:
            log.info('<<< Copying file ... >>>')
            if len(file_list) > 0:
                peform_copy(file_list)
            else:
                raise FileWatchError('Unexpected empty file_list')

        if config.archive_file:
            log.info('<<< Archiving file ... >>>')
            perform_archive()

        log.info('EXIT 0')

    except Exception as ex:
        print(ex)
        if log:
            log.error('<<<<< Error caught in file_watcher main() >>>>>')
            log.error(ex)
            log.error(traceback.format_exc())
        else:
            traceback.print_exc()
        sys.exit(875)

    else:
        log.info(
            f'<<<<< File Watcher Job ({args.job_name}) -- Completed Successfully at ( {str_now()} ) >>>>> '
        )

    finally:
        pass


if __name__ == '__main__':
    main()
