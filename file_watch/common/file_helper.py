from asyncio.windows_events import NULL
import boto3

import os
from os import DirEntry
import logging
import shutil
import fnmatch
import gzip
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, List, Dict


from file_watch.common import s3_helper
from file_watch.common.enum_const import PathType, Constant
from file_watch.core.config_core import ValidJobConfig


def get_log_file_path(job_name: str) -> str:
    """get logs absolute path from this module's path"""

    path = Path(__file__).parent.parent
    str_date = datetime.today().strftime('%Y-%m-%d')
    path = (
        path.joinpath(Constant.LOGS_RELATIVE_PATH).joinpath(f'{job_name}_{str_date}.log').absolute()
    )
    return str(path)


def get_last_modified(file_name: str, source_path: str) -> datetime:
    """return last modifed datetime for a single file"""
    
    try: 
        file_path = os.path.join(source_path, file_name)
        stats = os.stat(file_path)
    except: 
        return None
    return datetime.fromtimestamp(stats.st_mtime)

def trim_to_milliseconds(dt: datetime) -> datetime:
    """trim a microsecond-precision datetime to millisecopnd-precision datetime
        this is needed to compare a Windows OS file datetime vs SQL Server datetime
    """

    formatted_datetime = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    trimmed_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S.%f')
    return trimmed_datetime

def get_file_size(file_name: str, source_path: str) -> int:
    """return file size for a single file"""

    try:
        file_path = os.path.join(source_path, file_name)
        stats = os.stat(file_path)
    except:
        return None
    return stats.st_size


def get_files_dicts_on_local(
    source_path: str,
) -> Tuple[List[str], Dict[str, datetime], Dict[str, int]]:
    """get files from local or UNC path"""

    log = logging.getLogger()
    file_names = os.listdir(source_path)
    dup_path_list = [source_path] * len(file_names)
    log.debug('After getting all file_names from OS, before getting modified dates and sizes ... ')
    
    last_modified_list = list(map(get_last_modified, file_names, dup_path_list))
    size_list = list(map(get_file_size, file_names, dup_path_list))

    # dictionary comprehension
    date_dict = {file_names[i]: last_modified_list[i] for i in range(len(file_names))}
    size_dict = {file_names[i]: size_list[i] for i in range(len(file_names))}

    return (file_names, date_dict, size_dict)


def get_files(config: ValidJobConfig) -> Tuple[List[str], Dict[str, datetime], Dict[str, int]]:
    """get filename list based on source path type"""

    log = logging.getLogger()
    if config.effective_source_path_type == PathType.S3_PATH:
        # list files from s3 bucket
        log.debug('Preparing to get files from s3 bucket ... ')
        bucket, prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.source_path)
        files = s3_helper.get_files_on_s3(bucket, prefix)
        return files
    elif config.effective_source_path_type in [PathType.LOCAL_PATH, PathType.UNC_PATH]:
        # list files on local path or UNC path
        log.debug('Preparing to get files from source path  ... ')
        return get_files_dicts_on_local(config.source_path)
    else:
        raise ValueError('effective_source_path_type is not derived')


def copy_files_local_2_local(source_file_path: str, dest_file_path: str) -> None:
    """attempts to preserve file metadata such as last modifed date when copying
    including local path and UNC path"""

    shutil.copy2(source_file_path, dest_file_path)

def archive_files_local_2_local(source_file_path: str, dest_file_path: str) -> None:
    """archive/move files from UNC/local to UNC/local and append timestamp"""

    shutil.copy2(source_file_path, get_unique_archive_file_path(dest_file_path))

def get_unique_archive_file_path(full_filepath: str) -> str:
    """append '_{yyyyMMdd}_{HHmmssfff}.${ext}' to the original filenames for uniqueness """

    directory, filename_with_ext = os.path.split(full_filepath)
    filename, extension = os.path.splitext(filename_with_ext)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    new_filename = f'{filename}_{timestamp}{extension}'
    return os.path.join(directory, new_filename)

def get_unique_archive_file_name(filename_with_ext: str) -> str:
    """append '_{yyyyMMdd}_{HHmmssfff}.${ext}' to the original filenames for uniqueness """

    filename, extension = os.path.splitext(filename_with_ext)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    new_filename = f'{filename}_{timestamp}{extension}'
    return new_filename

def copy_file_by_path_type(config: ValidJobConfig, file_name: str) -> None:
    """select corresponding function to call based on source and destination PathType"""

    assert config.target_path is not None  # make mypy happy

    if config.effective_source_path_type == PathType.S3_PATH:
        if config.effective_target_path_type == PathType.S3_PATH:
            # s3 to s3 copy
            source_bucket, source_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.source_path)
            copy_bucket, copy_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.target_path)
            source_key = source_prefix + file_name
            copy_key = copy_prefix + file_name
            s3_helper.copy_files_s3_2_s3(source_bucket, source_key, copy_bucket, copy_key)

        else:
            # s3 to local/UNC download
            source_bucket, source_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.source_path)
            source_key = source_prefix + file_name
            copy_file_path = Path(config.target_path).joinpath(file_name).absolute()
            log = logging.getLogger()
            log.debug(f'S3 to local/UNC copy target path using absolute(): {str(copy_file_path)} ')            
            s3_helper.copy_files_s3_2_local(source_bucket, source_key, str(copy_file_path))
    else:
        if config.effective_target_path_type == PathType.S3_PATH:
            # local/UNC to s3 upload
            source_file_path = Path(config.source_path).joinpath(file_name).absolute()
            copy_bucket, copy_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.target_path)
            copy_key = copy_prefix + file_name
            s3_helper.copy_files_local_2_s3(str(source_file_path), copy_bucket, copy_key)

        else:
            # local to local copy including UNC path
            source_file_path = Path(config.source_path).joinpath(file_name).absolute()
            copy_file_path = Path(config.target_path).joinpath(file_name).absolute()
            copy_files_local_2_local(str(source_file_path), str(copy_file_path))


def copy_files(config: ValidJobConfig, files: list) -> None:
    """copy files from source_path to target_path"""

    log = logging.getLogger()
    for file_name in files:
        log.info(f'Copying {file_name} ... ')
        copy_file_by_path_type(config, file_name)
    log.info(f'{len(files)} file(s) successfully copied')


def archive_file_by_path_type(config: ValidJobConfig, file_name: str) -> None:
    """select corresponding function to call based on source and destination PathType"""

    assert config.archive_path is not None  # make mypy happy

    if config.effective_source_path_type == PathType.S3_PATH:
        if config.effective_archive_path_type == PathType.S3_PATH:
            # s3 to s3 copy
            source_bucket, source_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.source_path)
            archive_bucket, archive_prefix = s3_helper.get_s3_bucket_prefix_by_uri(
                config.archive_path
            )
            source_key = source_prefix + file_name
            archive_key = archive_prefix + get_unique_archive_file_name(file_name)
            s3_helper.copy_files_s3_2_s3(source_bucket, source_key, archive_bucket, archive_key)

        else:
            # s3 to local download
            source_bucket, source_prefix = s3_helper.get_s3_bucket_prefix_by_uri(config.source_path)
            source_key = source_prefix + file_name
            archive_file_path = Path(config.archive_path).joinpath(file_name).absolute()
            s3_helper.copy_files_s3_2_local(source_bucket, source_key, get_unique_archive_file_name(str(archive_file_path)))

    else:
        if config.effective_archive_path_type == PathType.S3_PATH:
            # local to s3 upload and remove from source_path !!!
            source_file_path = Path(config.source_path).joinpath(file_name).absolute()
            archive_bucket, archive_prefix = s3_helper.get_s3_bucket_prefix_by_uri(
                config.archive_path
            )
            archive_key = archive_prefix + get_unique_archive_file_name(file_name)
            s3_helper.copy_files_local_2_s3(str(source_file_path), archive_bucket, archive_key)
            os.remove(source_file_path)

        else:
            # local to local move including UNC path (removing from source_path!!!)
            source_file_path = Path(config.source_path).joinpath(file_name).absolute()
            archive_file_path = Path(config.archive_path).joinpath(file_name).absolute()
            archive_files_local_2_local(str(source_file_path), str(archive_file_path))
            os.remove(source_file_path)


def verify_local_files(file_names: List[str], file_path: str) -> bool:
    for file_name in file_names:
        if Path(file_path).joinpath(file_name).is_file():
            continue
        else:
            log = logging.getLogger()
            log.debug(f'file dos not exist in "{file_path}": {file_names}')
            return False

    return True


def archive_files(config: ValidJobConfig, files: list) -> None:
    """archive/copy files from source_path to archive_path"""

    log = logging.getLogger()
    for file_name in files:
        log.info(f'Archiving {file_name} ... ')
        archive_file_by_path_type(config, file_name)
    log.info(f'{len(files)} file(s) successfully archived')


def decompress_files(config: ValidJobConfig, files: list) -> None:
    """decompress files from target path and clean"""

    log = logging.getLogger()
    i: int = 0
    for file_name in files:
        if file_name.lower().endswith('.gz') and '.gz' in config.files_decompress:
            target_file_path_gz = str( Path(config.target_path).joinpath(file_name).absolute())
            log.info(f'Decompressing {target_file_path_gz} ... ')
            target_file_path = target_file_path_gz[:-3]
            fp = open(target_file_path, "wb")
            with gzip.open(target_file_path_gz, "rb") as f:
                bindata = f.read()
            fp.write(bindata)
            fp.close()
            log.info(f'Decompress .gz Success: {target_file_path} ') 
            i = i+1
            os.remove(target_file_path_gz)
            log.info(f'Deleted original compressed file: {target_file_path_gz}  ') 
        elif file_name.lower().endswith('.zip') and '.zip' in config.files_decompress:
            target_file_path_zip = str(Path(config.target_path).joinpath(file_name).absolute())
            log.info(f'Decompressing {target_file_path_zip} ... ')
            shutil.unpack_archive(target_file_path_zip, config.target_path, 'zip')
            i = i+1
            log.info(f'Decompress .zip Success ') 
            os.remove(target_file_path_zip)
            log.info(f'Deleted original compressed file: {target_file_path_zip}  ') 

    log.info(f'{i} file(s) successfully decompressed')


def get_mode_date(entry: DirEntry) -> datetime:
    """get modified date from DirEntry"""
    return datetime.fromtimestamp(entry.stat(follow_symlinks=False).st_mtime)


def match_pattern(patterns: list, entry: DirEntry) -> bool:
    """check if file_name matches pattern"""

    for pat in patterns:
        if fnmatch.fnmatch(entry.name, pat):
            return True
    else:
        return False


def match_age(age: int, entry: DirEntry) -> bool:
    """check if file_age matches age criteria"""

    mod_date = get_mode_date(entry)
    delta: timedelta = datetime.now() - mod_date
    if delta.days >= age:
        return True
    else:
        return False


def may_clean_file(entry: DirEntry, patterns: list, age: int) -> None:
    """clean up a file only if criteria are all matched"""

    if not match_pattern(patterns, entry):
        return
    if not match_age(age, entry):
        return

    log = logging.getLogger()
    mod_date = get_mode_date(entry)
    log.debug(f'deleting "{entry.name}": last modified on {mod_date}')
    try:
        os.remove(entry.path)
    except Exception as ex:
        log.debug(ex)
