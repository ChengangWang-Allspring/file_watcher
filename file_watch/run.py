import sys
import traceback
import logging
import logging.config


from file_watch.service import prepare
from file_watch.service import stage
from file_watch.helper.common import Setting


def main():

    try:
        # parse arguments
        prepare.parse_args()

        # config logging
        prepare.config_logging()

        # initialize job config along with logger
        prepare.load_job_config()

        # perform watch
        stage.perform_watch()

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
