#########################################################
# file_watcher
# Allspring Global Investments
# version: 1.0.0
# author: cwang@allspringglobal.com
#########################################################

import argparse
import sys
from datetime import datetime
import traceback
import logging
import logging.config
from pathlib import Path
from commons import *
from config_man import *
import actions
import helpers



def parse_args():
    """
    File watcher utility. Check README.md
    Example useage:
        python main.py -d -env prod -job <job_name>
    required python version 3.11
    <job_name>.yml configuration file has to be in /conf folder.
    """

    parser = argparse.ArgumentParser(
        description="File_watch utility built in Python. Please refer to README for usage"
    )
    parser.add_argument('-job', dest='job_name', required=True, help='job_name file without .yml extension')
    parser.add_argument('-env', dest='environment', help='runtime environment [DEV | UAT | PROD ]')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='force DEBUG log message')
    return parser.parse_args()



def str_now() -> str :
    return datetime.now().strftime("%c")

def set_log_level(log, debug:bool) -> None:
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    log.setLevel(level)
    for handler in log.handlers:
        handler.setLevel(level)        


def main():

    log = None

    try: 
        #parse arguments
        args = parse_args()

        #check if yaml config exists
        config_path: Path = helpers.get_job_config_path(args.job_name)
        if(not config_path.exists()):
            raise commons.JobConfigError(f'Cannot find {args.job_name}.yml config file in conf/')

        # initialize job config along with logger
        config = ConfigManager.get_config(args.job_name, config_path.resolve())   
        config.force_debug = args.debug
        config.force_env = args.environment
        log = logging.getLogger()
        set_log_level(log, config.force_debug)

        log.info(f'Initializing file watcher ...')
        log.info(f'Job config path: {config_path} ...')
        log.info(f'Log file path: {config.LOG_FILE_PATH} ...')

        log.info(f'Loading job config: {args.job_name} ...')
        if config.force_env:
            print(f'Runtime Environment: {args.environment}')        
        
        # parse job config
        log.info('........................................................')
        log.info(f'<<<<< File Watcher Job ({args.job_name}) -- Started at ( {str_now()} ) >>>>> ')
        log.info('........................................................')
        log.info('<<< Parsing all variables in the job configuration >>>')
        config.parse_config()
        config.print_config()
        if config.force_env:
            log.info('........................................................')
            log.info('<<< Parsing variables overides >>>')
            config.parse_env_overrides()
            log.info('<<< Effective variables in the job configuration >>>')
            config.print_config()



        file_list = []
        if(config.watch_file) :
            log.info('<<< Watching file ... >>>')            
            file_list = actions.perform_watch()

        if(config.copy_file):
            log.info('<<< Copying file ... >>>') 
            if len(file_list) > 0: 
                actions.peform_copy(file_list)
            else:
                raise commons.FileWatchError('Unexpected empty file_list')

        if(config.archive_file):
            log.info('<<< Archiving file ... >>>')  
            actions.perform_archive()    

        log.info('EXIT 0')
        
    except Exception as ex:
        if log:
            log.error('<<<<< Error caught in file_watcher main() >>>>>')
            log.error(ex)
            log.error(traceback.format_exc())            
        else:
            traceback.print_exc()
        sys.exit(875)

    else:
        log.info(f'<<<<< File Watcher Job ({args.job_name}) -- Completed Successfully at ( {str_now()} ) >>>>> ')

    finally:
        pass



if __name__ == "__main__":
    main()
