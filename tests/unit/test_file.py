import pytest
import os
from pathlib import Path
from datetime import datetime, timedelta
import tempfile

from file_watch.common import file_helper
from file_watch.core import core_helper
from file_watch.common.enum_const import PathType


@pytest.fixture
def patch_datetime_now(monkeypatch):
    """datetime.now() mocked to return 2022-03-08 12:30pm"""

    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2022, 6, 21, 10, 30)

    monkeypatch.setattr(core_helper, 'datetime', mydatetime)


@pytest.mark.file_test
def test_get_log_file_path():
    job_name = 'test_job'
    str_date = datetime.today().strftime('%Y-%m-%d')
    home = Path(__file__).parent.parent.parent
    log_path = home.joinpath(f'file_watch/logs/{job_name}_{str_date}.log').resolve()

    assert file_helper.get_log_file_path('test_job') == str(log_path)


@pytest.mark.file_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('prefix_{yyyyMMdd}_surfix.csv', 'prefix_20220621_surfix.csv'),
        ('prefix_{today}_surfix.csv', 'prefix_20220621_surfix.csv'),
        ('prefix_{todayPm}_surfix.csv', 'prefix_20220620_surfix.csv'),
        ('prefix_{prevWeekDay}_surfix.csv', 'prefix_20220620_surfix.csv'),
        ('prefix_{prevDay:MM-dd-yyyy}_surfix.csv', 'prefix_06-20-2022_surfix.csv'),
        ('prefix_{prevBizDay:yyyy_MM_dd}_surfix.csv', 'prefix_2022_06_17_surfix.csv'),
        ('prefix_{lastBizDayOfLastMnth:yyMMdd}_surfix.csv', 'prefix_220531_surfix.csv'),
        ('prefix_{lastDayOfLastMnth}_surfix.csv', 'prefix_20220531_surfix.csv'),
        ('prefix_{firsBizDayOfMnth}_surfix.csv', 'prefix_20220601_surfix.csv'),
        ('prefix_{firsDayOfMnth}_surfix.csv', 'prefix_20220601_surfix.csv'),
    ],
)
def test_parse_file_name(patch_datetime_now, txt_input, expected):
    assert core_helper.parse_file_name(txt_input) == expected


@pytest.mark.file_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        (r'C:\cwang\test', PathType.LOCAL_PATH),
        ('s3://mybucket/mypath', PathType.S3_PATH),
        (r'\\myshare\apps$\myfolder', PathType.UNC_PATH),
        (r'adb:\wgdg$!@#$$%', PathType.NONE),
    ],
)
def test_validate_path_type(txt_input, expected):
    assert core_helper.validate_path_type(txt_input) == expected


def test_get_last_modified(tmp_path):
    start_time = datetime.now()
    fd, file_path = tempfile.mkstemp(dir=tmp_path)
    mod_time = file_helper.get_last_modified(Path(file_path).stem, tmp_path)
    os.close(fd)
    os.remove(file_path)
    assert (mod_time - start_time) < timedelta(seconds=1)


def test_get_file_size(tmp_path):
    fd, file_path = tempfile.mkstemp(dir=tmp_path)
    file_size = file_helper.get_file_size(Path(file_path).stem, tmp_path)
    os.close(fd)
    os.remove(file_path)
    assert file_size == 0


def test_get_files_dicts_on_local(tmp_path):
    start_time = datetime.now()
    fd1, file_path_1 = tempfile.mkstemp(dir=tmp_path)
    fd2, file_path_2 = tempfile.mkstemp(dir=tmp_path)
    files, date_dict, size_dict = file_helper.get_files_dicts_on_local(tmp_path)
    os.close(fd1)
    os.close(fd2)
    os.remove(file_path_1)
    os.remove(file_path_2)
    assert Path(file_path_1).stem in files
    assert Path(file_path_2).stem in files
    for date in date_dict.values():
        assert (date - start_time) < timedelta(seconds=1)
    for size in size_dict.values():
        assert size == 0
