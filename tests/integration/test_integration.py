import pytest
import boto3


import time
import threading
from typing import List
from datetime import datetime
from pathlib import Path


from file_watch import app
from file_watch.core import config_factory, config_core
from file_watch.common.enum_const import JobConfigType, PathType
from file_watch.common.setting import Setting
from file_watch.common import s3_helper


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


def mock_deliver_local_files(file_names: List[str], file_count: int, source_path: str):
    """special logic to deliver mock deliver files to local path based on file_name pattern list"""

    print(f'############# Mock local file delivery thread started ...')
    print(f'############# file_names: {file_names}')
    print(f'############# file_count: {file_count}')
    print(f'############# source_path: {source_path}')
    print(f'############# Sleep 5 seconds before delivering mock files ...')

    time.sleep(5)

    delivered_count: int = 0
    # a little tricky, sometime file_names in list format without wild card, sometime file_name in wild-card format
    while delivered_count < file_count:
        asterisk_name = None
        for file in file_names:
            if '*' in file:
                asterisk_name = file
            else:
                print(
                    f'############# Attemping to deliver mock file in "{source_path}": {file} ...'
                )
                Path(source_path).joinpath(file).touch(exist_ok=True)
                print(f'############# Mock file delivered in "{source_path}": {file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            if asterisk_name is None:
                raise Exception("file_names error! Cannot mock deliver enough files!!!")
            num_files = file_count - delivered_count

            for i in range(num_files):
                real_file = asterisk_name.replace('*', str(i))
                print(
                    f'############# Attemping to deliver mock file in "{source_path}": {real_file} ...'
                )
                Path(source_path).joinpath(real_file).touch(exist_ok=True)
                print(f'############# Mock file delivered in "{source_path}": {real_file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            raise Exception("file_names error in job configuration. Cannot deliver enough files!!!")


def mock_deliver_s3_files(file_names: List[str], file_count: int, source_path: str):
    """special logic to deliver mock deliver files to s3 bucket based on file_name pattern list"""

    print(f'############# Mock local file delivery thread started ...')
    print(f'############# file_names: {file_names}')
    print(f'############# file_count: {file_count}')
    print(f'############# source_path: {source_path}')
    bucket, key = s3_helper.get_s3_bucket_prefix_by_uri(source_path)
    print(f'############# bucket: {bucket}')
    print(f'############# key: {key}')
    print(f'############# Sleep 5 seconds before delivering mock files ...')

    time.sleep(5)

    delivered_count: int = 0
    # a little tricky, sometime file_names in list format without wild card, sometime file_name in wild-card format
    while delivered_count < file_count:
        asterisk_name = None
        for file in file_names:
            if '*' in file:
                asterisk_name = file
            else:
                print(
                    f'############# Attemping to deliver mock file in "{source_path}": {file} ...'
                )
                Path(source_path).joinpath(file).touch(exist_ok=True)
                s3 = boto3.resource('s3')
                source_path_str = str(Path(source_path).joinpath(file).resolve())
                key = key + file
                s3.meta.client.upload_file(source_path_str, bucket, key)
                print(f'############# Mock file delivered in "{source_path}": {file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            if asterisk_name is None:
                raise Exception("file_names error! Cannot mock deliver enough files!!!")
            num_files = file_count - delivered_count

            for i in range(num_files):
                real_file = asterisk_name.replace('*', str(i))
                print(
                    f'############# Attemping to deliver mock file in "{source_path}": {real_file} ...'
                )
                Path(source_path).joinpath(real_file).touch(exist_ok=True)
                s3 = boto3.resource('s3')
                source_path_str = str(Path(source_path).joinpath(real_file).resolve())
                key = key + real_file
                s3.meta.client.upload_file(source_path_str, bucket, key)
                print(f'############# Mock file delivered in "{source_path}": {real_file} ...')
                delivered_count += 1

        if delivered_count < file_count:
            raise Exception("file_names error in job configuration. Cannot deliver enough files!!!")


@pytest.mark.parametrize(
    'job_name, keys',
    [
        ('INTGR_TEST_1', ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_2', ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_3', ['Completed Successfully', 'EXIT 0']),
        ('INTGR_TEST_4', ['Completed Successfully', 'EXIT 0']),
    ],
)
def test_execute_job(patch_datetime_now, job_name: str, keys: List[str]):
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

    mock_file_deliver_thread = None
    if source_path_type == PathType.LOCAL_PATH:
        mock_file_deliver_thread = threading.Thread(
            target=mock_deliver_local_files, args=(file_names, file_count, source_path)
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

    # TODO, check keys exists in log
    assert exit_code == 0
