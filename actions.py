import logging
import time
import os
import fnmatch
from config_man import ConfigManager
import helpers
import commons


def perform_watch() -> list:
    ##########################################
    # File Watch - <while> loop Logic
    ##########################################
    config = ConfigManager.get_config()
    log = logging.getLogger()
    log.info(f'<<< Looking for file(s) ({config.file_name}) from ({config.source_path}) >>>')   
    file_count: int = 0
    poll_attempt: int = 0
    while True:
        poll_attempt += 1
        files = get_files()
        match = []
        if len(files) > 0:
            for filename in config.file_name:
                log.debug(f'checking {filename}')
                match += fnmatch.filter(files, filename)
        # remove duplicate from the list 
        if len(match) > 0:
            match = [*set(match)] 

        if len(match) >= config.file_count:
            log.info(f'Files Were Found In Location [ {len(match)} out of {config.file_count} ] -- {config.source_path}')
            log.info(match)
            return match
        else:
            log.info(f'No file (or Not Enough files [ {len(match)} out of {config.file_count} ]) Were Found - Attempt {poll_attempt} out of {config.look_time} -- Sleeping for {config.sleep_time} Seconds --')
            time.sleep(config.sleep_time)
            if poll_attempt >= config.look_time:
                log.error(f'No File (or Not Enough Files [ 0 out of {config.file_count} ]) were Found in the requested amount of times.')
                raise commons.FileWatchTimeOutError('Maximum polling times reached!')



def get_files() -> list:
    ##############################################
    #  return filename list based on source type
    ##############################################
    config = ConfigManager.get_config()
    log = logging.getLogger()
    if config.is_source_s3:
        # list files from s3 bucket
        log.debug('Preparing to get files from s3 bucket ... ')
        files = helpers.get_files_on_s3(config.source_s3_bucket, config.source_s3_prefix)
        return files
    elif config.source_path:
        # list files on local path or UNC path
        log.debug('Preparing to get files from source path  ... ')
        return os.listdir(config.source_path)
    else:
        # this should be handled in JobConfig parse
        raise commons.JobConfigError('Cannot resolve source.')

def peform_copy(file_list: list):
    ####################################################################
    #  copy files from effective source to effective target location
    ####################################################################
    
    pass

def perform_archive():
    ####################################################################
    #  archive files from effective source to effective archive location
    ####################################################################    
    pass