import pytest
from pathlib import Path
from datetime import datetime

from file_watch.common import file_helper
from file_watch.core import core_helper
from file_watch.common.enum_const import PathType
from file_watch.common import file_helper


@pytest.fixture
def patch_datetime_now(monkeypatch):
    """datetime.now() mocked to return 2022-03-08 12:30pm"""

    class mydatetime:
        @classmethod
        def now(cls):
            return datetime(2022, 6, 21, 10, 30)

    monkeypatch.setattr(core_helper, 'datetime', mydatetime)


@pytest.mark.helper_test
def test_get_log_file_path():
    job_name = 'test_job'
    str_date = datetime.today().strftime('%Y-%m-%d')
    home = Path(__file__).parent.parent
    log_path = home.joinpath(f'file_watch/logs/{job_name}_{str_date}.log').resolve()

    assert file_helper.get_log_file_path('test_job') == str(log_path)


@pytest.mark.helper_test
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


@pytest.mark.helper_test
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


@pytest.mark.helper_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('s3://mybucket/mypath/', ['mybucket', 'mypath/']),
        ('s3://another_bucket/test/inbound/', ['another_bucket', 'test/inbound/']),
    ],
)
def test_get_s3_bucket_prefix_by_uri(txt_input, expected):
    assert file_helper.get_s3_bucket_prefix_by_uri(txt_input) == expected
