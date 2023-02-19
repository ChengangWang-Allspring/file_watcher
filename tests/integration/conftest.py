import pytest
import boto3

import os
from pathlib import Path

from file_watch.common import s3_helper

LOCAL_SOURCE_PATH = r'c:\temp\tests\integration\source'
LOCAL_INBOUND_PATH = r'c:\temp\tests\integration\inbound'
LOCAL_ARCHIVE_PATH = r'c:\temp\tests\integration\archive'

S3_SOURCE_PATH = 's3://s3-agtps01-use-dev/tests/integration/source/'
S3_INBOUND_PATH = 's3://s3-agtps01-use-dev/tests/integration/inbound/'
S3_ARCHIVE_PATH = 's3://s3-agtps01-use-dev/tests/integration/archive/'


def reset_local_folders(local_path_str: str):
    my_path = Path(local_path_str)
    if my_path.exists():
        print(f'############# attempt to clean up files in local path: {local_path_str}')
        for f in os.listdir(local_path_str):
            os.remove(str(my_path.joinpath(f).resolve()))
    else:
        my_path.mkdir(parents=True, exist_ok=True)


def reset_all_local_folders():
    """reset local folders needed for file_watch integration testing"""

    reset_local_folders(LOCAL_SOURCE_PATH)
    reset_local_folders(LOCAL_INBOUND_PATH)
    reset_local_folders(LOCAL_ARCHIVE_PATH)


def reset_s3_folder(s3_uri: str):
    """reset s3 bucket folders needed for file_watch integration testing"""

    s3 = boto3.client('s3')
    print(f'############# attempt to clean up files in s3 url: {s3_uri}')
    bucket, prefix = s3_helper.get_s3_bucket_prefix_by_uri(s3_uri)
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' in response:
        for object in response['Contents']:
            print('############# Deleting', object['Key'])
            s3.delete_object(Bucket=bucket, Key=object['Key'])


def reset_all_s3_folders():
    reset_s3_folder(S3_SOURCE_PATH)
    reset_s3_folder(S3_INBOUND_PATH)
    reset_s3_folder(S3_ARCHIVE_PATH)


@pytest.fixture(scope="function", autouse=True)
def auto_resource():
    print('')  # extra line break to seperate for pytest message
    reset_all_local_folders()
    reset_all_s3_folders()

    yield

    print('')  # extra line break so that PASSED is easy to see
    reset_all_local_folders()
    reset_all_s3_folders()
