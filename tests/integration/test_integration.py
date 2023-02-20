import pytest
import boto3


import time
import os
import shutil
import threading
from typing import List
from datetime import datetime
from pathlib import Path


from file_watch import app
from file_watch.core import config_factory, config_core
from file_watch.common.enum_const import JobConfigType, PathType
from file_watch.common.setting import Setting
from file_watch.common import s3_helper, file_helper
from tests.integration.conftest import LOCAL_TEMP_PATH


def mock_systime() -> datetime:
    return datetime(2022, 6, 21, 10, 30)


@pytest.fixture()
def patch_datetime_now(monkeypatch):
    """monkeypatch to override datetime.now() in core_helper to use mock_systime()"""

    class mydatetime:
        @classmethod
        def now(cls):
            return mock_systime()

    # turn off the moneypatch and use current datetime.now()
    # monkeypatch.setattr(core_helper, 'datetime', mydatetime)


def mock_deliver_local_files(
    file_names: List[str], file_count: int, source_path: str, patch_mod_date: bool
):
    """special logic to deliver mock deliver files to local path based on file_name pattern list"""

    print(f'############# Mock local file delivery thread started ...')
    print(f'############# file_names: {file_names}')
    print(f'############# file_count: {file_count}')
    print(f'############# source_path: {source_path}')
    print(f'############# Sleep 5 seconds before delivering mock files ...')

    time.sleep(3)

    delivered_count: int = 0
    # a little tricky, sometime file_names in list format without wild card, sometime file_name in wild-card format
    while delivered_count < file_count:
        asterisk_name = None
        for file in file_names:
            if '*' in file:
                asterisk_name = file
            else:
                print(
                    f'############# Attemping to deliver mock file to "{source_path}": {file} ...'
                )
                print(f'############### patch_mod_date: {patch_mod_date} ')
                if not patch_mod_date:
                    Path(source_path).joinpath(file).touch(exist_ok=True)
                else:
                    Path(LOCAL_TEMP_PATH).joinpath(file).touch(exist_ok=True)
                    str_file_path = str(Path(LOCAL_TEMP_PATH).joinpath(file).resolve())
                    os.utime(str_file_path, (1330712280, 1330712292))
                    shutil.move(str_file_path, Path(source_path).joinpath(file).resolve())
                print(f'############# Mock file delivered to "{source_path}": {file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            if asterisk_name is None:
                raise Exception("file_names error! Cannot mock deliver enough files!!!")
            num_files = file_count - delivered_count

            for i in range(num_files):
                real_file = asterisk_name.replace('*', str(i))
                print(
                    f'############# Attemping to deliver mock file to "{source_path}": {real_file} ...'
                )
                print(f'############### patch_mod_date: {patch_mod_date} ')
                if not patch_mod_date:
                    Path(source_path).joinpath(real_file).touch(exist_ok=True)
                else:
                    Path(LOCAL_TEMP_PATH).joinpath(real_file).touch(exist_ok=True)
                    str_file_path = str(Path(LOCAL_TEMP_PATH).joinpath(real_file).resolve())
                    os.utime(str_file_path, (1330712280, 1330712292))
                    shutil.move(str_file_path, Path(source_path).joinpath(real_file).resolve())
                print(f'############# Mock file delivered to "{source_path}": {real_file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            raise Exception("file_names error in job configuration. Cannot deliver enough files!!!")


def mock_deliver_s3_files(file_names: List[str], file_count: int, source_path: str):
    """special logic to deliver mock deliver files to s3 bucket based on file_name pattern list"""

    print(f'############# Mock local file delivery thread started ...')
    print(f'############# file_names: {file_names}')
    print(f'############# file_count: {file_count}')
    print(f'############# source_path: {source_path}')
    bucket, prefix = s3_helper.get_s3_bucket_prefix_by_uri(source_path)
    print(f'############# bucket: {bucket}')
    print(f'############# prefix: {prefix}')
    print(f'############# Sleep 5 seconds before delivering mock files ...')

    time.sleep(3)

    delivered_count: int = 0
    # a little tricky, sometime file_names in list format without wild card, sometime file_name in wild-card format
    while delivered_count < file_count:
        asterisk_name = None
        for file in file_names:
            if '*' in file:
                asterisk_name = file
            else:
                print(
                    f'############# Attemping to deliver mock file to "{source_path}": {file} ...'
                )
                Path(LOCAL_TEMP_PATH).joinpath(file).touch(exist_ok=True)
                s3 = boto3.resource('s3')
                source_path_str = str(Path(LOCAL_TEMP_PATH).joinpath(file).resolve())
                key = prefix + file
                s3.meta.client.upload_file(source_path_str, bucket, key)
                print(f'############# Mock file delivered to "{source_path}": {file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            if asterisk_name is None:
                raise Exception("file_names error! Cannot mock deliver enough files!!!")
            num_files = file_count - delivered_count

            for i in range(num_files):
                real_file = asterisk_name.replace('*', str(i))
                print(
                    f'############# Attemping to deliver mock file to "{source_path}": {real_file} ...'
                )
                Path(LOCAL_TEMP_PATH).joinpath(real_file).touch(exist_ok=True)
                s3 = boto3.resource('s3')
                source_path_str = str(Path(LOCAL_TEMP_PATH).joinpath(real_file).resolve())
                key = prefix + real_file
                s3.meta.client.upload_file(source_path_str, bucket, key)
                print(f'############# Mock file delivered to "{source_path}": {real_file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            raise Exception("file_names error in job configuration. Cannot deliver enough files!!!")


def keys_in_log(log_file_path: str, keys: List[str]) -> bool:
    """check if given list of keys are in the log file"""

    for key in keys:
        with open(log_file_path, 'r') as file:
            # read all content from a file using read()
            content = file.read()
            # check if string present or not
            if key not in content:
                return False
    return True


""" 
        # Below are backup parameters
        # TEST_8 has hard coded logic to modify atime and mtime of a file to minic past last modified date

        ('INTGR_TEST_1', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_2', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_3', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_4', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_5', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_6', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_7', 875, ['not reaching min_size', 'Maximum polling times']),

"""


@pytest.mark.parametrize(
    'job_name, expected_exit_code, log_keys',
    [
        ('INTGR_TEST_1', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_2', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_3', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_4', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_5', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_6', 0, ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_7', 875, ['not reaching min_size', 'Maximum polling times']),
    ],
)
def test_execute_job(
    patch_datetime_now, job_name: str, expected_exit_code: int, log_keys: List[str]
):
    """iterate to test each jobs that are defined by the above prametrize"""

    # prepare job attributes for mocking file delivery thread
    Setting.db_profile = 'test'
    config_dict: dict = config_factory.ConfigFactory.get_config_dict(
        job_name, JobConfigType.DB_CONFIG
    )
    config = config_core.ValidJobConfig(**config_dict)
    file_names: List[str] = config.effective_file_names
    file_count: int = config.file_count
    source_path: str = config.source_path
    source_path_type: PathType = config.effective_source_path_type
    log_file_path = file_helper.get_log_file_path(job_name)

    mock_file_deliver_thread = None
    if source_path_type == PathType.LOCAL_PATH:
        patch_mode_date = False
        if job_name == 'INTGR_TEST_8':  # hard coded logic to patch modified date for Test_8 files
            patch_mode_date = True
        mock_file_deliver_thread = threading.Thread(
            target=mock_deliver_local_files,
            args=(file_names, file_count, source_path, patch_mode_date),
        )
    elif source_path_type == PathType.S3_PATH:
        mock_file_deliver_thread = threading.Thread(
            target=mock_deliver_s3_files, args=(file_names, file_count, source_path)
        )
    else:
        raise Exception(f'cannot detect source_path_type: {source_path_type} ')

    mock_file_deliver_thread.start()  # start a separate thread to mock file delivery

    exit_code: int = app.run(['-m file_watch', '--db', 'test', job_name, '--debug'])

    mock_file_deliver_thread.join()  # wait for mock file delivery thread to finish

    # check exit code
    assert exit_code == expected_exit_code
    # check log keys
    assert keys_in_log(log_file_path, log_keys) == True
