import sys
import traceback
import logging
import logging.config
from typing import List


from file_watch.stage import finish, prepare, action
from file_watch.common.enum_const import Constant


def run(argv: List[str]) -> int:
    try:
        # parse arguments
        prepare.parse_args_to_settings(argv)

        # config logging
        prepare.config_logging()

        # welcome
        prepare.welcome()

        # initialize job config along with logger
        prepare.load_job_config()

        # must perform watch
        files: List[str] = action.perform_watch()

        # may perform clear readonly
        action.may_clear_readonly(files)

        # may perform copy
        action.may_peform_copy(files)

        # may perform decompress
        action.may_peform_decompress(files)

        # may perform archive
        action.may_perform_archive(files)

        # verify files
        finish.may_verify(files)

        # cleanup
        finish.cleanup()

        return 0

    except Exception as ex:
        log = logging.getLogger()
        log.error('<<<<< Error caught in file_watcher main() >>>>>')
        log.error(ex)
        log.debug(type(ex).__name__)
        log.debug(traceback.format_exc())
        return 875


if __name__ == '__main__':
    run(sys.argv)
