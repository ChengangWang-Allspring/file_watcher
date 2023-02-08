import boto3
import botocore.exceptions
import yaml

import os
import logging
import shutil
from pathlib import Path


from pm_watch.helper import common
from pm_watch.helper.common import PathType, JobConfigError
from pm_watch.core.config_core import ValidJobConfig


def read_yml_config(job_name: str) -> dict:
    try:
        yml_config_path = common.get_yml_file_path(job_name)
        with open(yml_config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return config_dict
    except Exception as ex:
        ex.add_note(f'Error reading job config yml file: {yml_config_path}')
        raise ex


def get_files_on_s3(my_bucket: str, my_prefix: str) -> list:
    """use boto3 s3 client and function list_objects_v2
    to retieve list of filenames (without prefix) from s3
    """

    log = logging.getLogger()
    try:
        log.debug('Setting up boto3 s3 client ... ')
        s3 = boto3.client('s3')
        log.debug('Sending request using list_objects_v2 ... ')
        # get AWS response in a dictionary object
        response = s3.list_objects_v2(Bucket=my_bucket, Prefix=my_prefix)
        log.debug('Parsing contents in response ... ')
        if 'Contents' in response:
            # get list of file objects by key <Contents>
            contents = response['Contents']
            # list comprehension to get pure filename list without prefix
            # log.debug(f'Total count in contents including prefix: {len(contents)}')
            # log.debug(contents)
            files = [
                item['Key'].replace(my_prefix, '') for item in contents if item['Key'] != my_prefix
            ]
            # log.debug(f'Pure filename list (count: {len(files)}) retrieved. ')
            return files
        else:
            log.debug(f'Cannot find <Contents> in response dictionary')
            return []
    except Exception as e:
        e.add_note('Internal Exception thrown during get_files_on_s3.')
        raise e


def get_s3_bucket_prefix_by_uri(url: str) -> list:
    """parse s3 bucket and prefix from s3 uri"""

    url = url.replace('s3://', '')
    bucket = url[: url.index('/')]
    prefix = url[url.index('/') + 1 :]
    return [bucket, prefix]


def get_files(config: ValidJobConfig) -> list:
    """get filename list based on source path type"""

    log = logging.getLogger()
    if config.effective_source_path_type == PathType.S3_PATH:
        # list files from s3 bucket
        log.debug('Preparing to get files from s3 bucket ... ')
        bucket, prefix = get_s3_bucket_prefix_by_uri(config.source_path)
        files = get_files_on_s3(bucket, prefix)
        return files
    elif config.effective_source_path_type in [PathType.LOCAL_PATH, PathType.UNC_PATH]:
        # list files on local path or UNC path
        log.debug('Preparing to get files from source path  ... ')
        return os.listdir(config.source_path)
    else:
        raise JobConfigError('effective_source_path_type is not derived')


def copy_files_local_2_local(src: str, dest: str):
    """attempts to preserve file metadata such as last modifed date when copying
    including local path and UNC path
    """
    shutil.copy2(src, dest)


def copy_files_s3_2_s3(gsrc: str, dest: str):
    """attempts to preserve file metadata such as last modifed date when copying
    including local path and UNC path
    """
    shutil.copy2(src, dest)


def copy_file_by_path_type(config: ValidJobConfig, file_name: str):
    """select corresponding function to call based on source and destination PathType"""

    if config.effective_source_path_type == PathType.S3_PATH:
        if config.effective_copy_path_type == PathType.S3_PATH:
            pass  # s3 to s3 copy
        else:
            pass  # s3 to local download
    else:
        if config.effective_copy_path_type == PathType.S3_PATH:
            pass  # local to s3 upload
        else:
            # local to local copy including UNC path
            src = Path(config.source_path).joinpath(file_name).resolve()
            dest = Path(config.copy_path).joinpath(file_name).resolve()
            copy_files_local_2_local(src, dest)


def copy_files(config: ValidJobConfig, files: list) -> None:
    """copy files from source_path to copy_path"""

    log = logging.getLogger()
    for file_name in files:
        log.info(f'Copying {file_name} ... ')
        copy_file_by_path_type(config, file_name)
    log.info(f'{len(files)} file(s) successfully copied')


def archive_file_by_path_type(config: ValidJobConfig, file_name: str):
    """select corresponding function to call based on source and destination PathType"""

    if config.effective_source_path_type == PathType.S3_PATH:
        if config.effective_archive_path_type == PathType.S3_PATH:
            pass  # s3 to s3 copy
        else:
            pass  # s3 to local download
    else:
        if config.effective_archive_path_type == PathType.S3_PATH:
            pass  # local to s3 upload
        else:
            # local to local copy including UNC path
            src = Path(config.source_path).joinpath(file_name).resolve()
            dest = Path(config.archive_path).joinpath(file_name).resolve()
            copy_files_local_2_local(src, dest)


def archive_files(config: ValidJobConfig, files: list) -> None:
    """archive/copy files from source_path to archive_path"""

    log = logging.getLogger()
    for file_name in files:
        log.info(f'Archiving {file_name} ... ')
        archive_file_by_path_type(config, file_name)
    log.info(f'{len(files)} file(s) successfully archived')
