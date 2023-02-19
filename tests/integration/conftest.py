import pytest

import shutil
from pathlib import Path

DATA_FIXTURE_PATH = 'data/fixtures'
LOCAL_INBOUND_PATH = 'data/inbound'
LOCAL_SOURCE_PATH = 'data/source'
LOCAL_ARCHIVE_PATH = 'data/archive'

S3_SOURCE_PATH = 's3://s3-agtps01-use-dev/tests/integration/source/'
S3_INBOUND_PATH = 's3://s3-agtps01-use-dev/tests/integration/inbound/'
S3_ARCHIVE_PATH = 's3://s3-agtps01-use-dev/tests/integration/archive/'

FILE_NAMES_WITH_SYSDATE = ('dummy_20220621_a.dat', 'dummy_20220621_b.dat')


def setup_local_folders():
    """setup local folders needed for file_watch integration testing"""
    base_path = Path(__file__).parent
    inbound_path = base_path.joinpath(LOCAL_INBOUND_PATH)
    source_path = base_path.joinpath(LOCAL_SOURCE_PATH)
    archive_path = base_path.joinpath(LOCAL_ARCHIVE_PATH)

    print('attempt to clean up local paths and recreate ... ')
    try:
        print(f'inbound_path: {inbound_path}')
        shutil.rmtree(inbound_path)
    except Exception as e:
        print(e)
    finally:
        inbound_path.mkdir()

    try:
        print(f'source_path: {source_path}')
        shutil.rmtree(source_path)
    except Exception as e:
        print(e)
    finally:
        source_path.mkdir()

    try:
        print(f'archive_path: {archive_path}')
        shutil.rmtree(archive_path)
    except Exception as e:
        print(e)
    finally:
        archive_path.mkdir()


def destroy_local_folders():
    """destroy local folders after testing is done"""
    base_path = Path(__file__).parent
    inbound_path = base_path.joinpath(LOCAL_INBOUND_PATH)
    source_path = base_path.joinpath(LOCAL_SOURCE_PATH)
    archive_path = base_path.joinpath(LOCAL_ARCHIVE_PATH)

    print('destroying local paths')
    try:
        print(f'inbound_path: {inbound_path}')
        shutil.rmtree(inbound_path)
    except Exception as e:
        print(e)

    try:
        print(f'source_path: {source_path}')
        shutil.rmtree(source_path)
    except Exception as e:
        print(e)

    try:
        print(f'archive_path: {archive_path}')
        shutil.rmtree(archive_path)
    except Exception as e:
        print(e)


@pytest.fixture(scope="session", autouse=True)
def auto_resource():
    setup_local_folders()

    yield

    destroy_local_folders()
