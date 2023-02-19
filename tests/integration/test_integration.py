import pytest
import time
import shutil
import threading
from typing import List
from datetime import datetime
from pathlib import Path

from file_watch import app
from file_watch.core import core_helper
from tests.integration import conftest


def mock_systime() -> datetime:
    return datetime(2022, 6, 21, 10, 30)


@pytest.fixture()
def patch_datetime_now(monkeypatch):
    """monkeypatch to override datetime.now() in core_helper to use mock_systime()"""

    class mydatetime:
        @classmethod
        def now(cls):
            return mock_systime()

    monkeypatch.setattr(core_helper, 'datetime', mydatetime)


def delayed_deliver_local_files():
    print('#' * 80)
    print(f'delivering files to local source folder: {conftest.LOCAL_SOURCE_PATH} ...')
    print('#' * 80)
    time.sleep(5)
    print('#' * 80)
    for file_name in conftest.FILE_NAMES_WITH_SYSDATE:
        fixture_file_path = (
            Path(__file__).parent.joinpath(conftest.DATA_FIXTURE_PATH).joinpath(file_name).resolve()
        )
        source_file_path = (
            Path(__file__).parent.joinpath(conftest.LOCAL_SOURCE_PATH).joinpath(file_name).resolve()
        )
        shutil.copy2(fixture_file_path, source_file_path)
        print(f'file delivered: {file_name}')
    print('#' * 80)


def delayed_deliver_s3_files(file_names: List[str], source_path: str):
    print(f'delivering to s3 source folder: {conftest.S3_SOURCE_PATH}')


@pytest.mark.parametrize(
    'job_name, keys',
    [
        ('test_901', ['Completed Successfully', 'EXIT 0']),
    ],
)
def test_execute_job_local_source(patch_datetime_now, job_name: str, keys: List[str]):
    file_deliver_thread = threading.Thread(target=delayed_deliver_local_files, args=())
    file_deliver_thread.start()
    exit_code: int = app.run(['-m file_watch', '--db', 'test', job_name, '--debug'])
    file_deliver_thread.join()
    assert exit_code == 0
