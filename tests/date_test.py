import pytest
from datetime import date, datetime, time

from file_watch.core import date_core as dp
from file_watch.core.date_core import cnv_csharp_date_fmt as cnv_fmt
from file_watch.core.date_core import datetime_offset as offset
from file_watch.core.date_core import split_date_token_fmt as split
from file_watch.core.date_core import parse_format_date as pf


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('yyyyMMdd', '%Y%m%d'),
        ('yyyy-MM-dd', '%Y-%m-%d'),
        ('MM/dd/yyyy', '%m/%d/%Y'),
        ('MMddyyyy', '%m%d%Y'),
        ('yyMMdd', '%y%m%d'),
        ('yyyy_MM_dd', '%Y_%m_%d'),
    ],
)
def test_cnv_csharp_date_fmt(txt_input, expected):
    assert cnv_fmt(txt_input) == expected


@pytest.mark.date_test
def test_dattime_offset():
    assert offset(datetime(2023, 1, 15, 12, 30, 00), -2, -6) == datetime(2023, 1, 13, 6, 30, 00)


@pytest.mark.date_test
def test_today():
    assert dp.today(datetime(2023, 1, 3)) == date(2023, 1, 3)


@pytest.mark.date_test
def test_today_pm():
    assert dp.today_pm(datetime(2023, 1, 17, 19)) == date(2023, 1, 16)
    assert dp.today_pm(datetime(2023, 1, 17, 21)) == date(2023, 1, 17)


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('2023-01-02', '2022-12-30'),
        ('2023-01-03', '2023-01-02'),
        ('2023-01-01', '2022-12-30'),
        ('2022-12-31', '2022-12-30'),
        ('2022-12-30', '2022-12-29'),
    ],
)
def test_prev_weekday(txt_input, expected):
    in_date = datetime.strptime(txt_input, '%Y-%m-%d')
    out_date = datetime.strptime(expected, '%Y-%m-%d').date()
    assert dp.prev_weekday(in_date) == out_date


@pytest.mark.date_test
def test_prev_day():
    assert dp.prev_weekday(datetime(2023, 1, 3)) == date(2023, 1, 2)


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('2023-11-13', '2023-11-09'),
        ('2023-11-12', '2023-11-09'),
        ('2023-11-11', '2023-11-09'),
        ('2023-11-10', '2023-11-09'),
        ('2023-11-14', '2023-11-13'),
        ('2022-05-31', '2022-05-27'),
    ],
)
def test_prev_bizday(txt_input, expected):
    in_date = datetime.strptime(txt_input, '%Y-%m-%d')
    out_date = datetime.strptime(expected, '%Y-%m-%d').date()
    assert dp.prev_bizday(in_date) == out_date


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('2022-08-15', '2022-07-29'),
        ('2022-07-15', '2022-06-30'),
        ('2022-03-15', '2022-02-28'),
        ('2021-06-15', '2021-05-28'),
    ],
)
def test_last_bizday_of_last_month(txt_input, expected):
    in_date = datetime.strptime(txt_input, '%Y-%m-%d')
    out_date = datetime.strptime(expected, '%Y-%m-%d').date()
    assert dp.last_bizday_of_last_month(in_date) == out_date


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('2022-07-15', '2022-06-30'),
        ('2022-06-15', '2022-05-31'),
        ('2022-03-15', '2022-02-28'),
    ],
)
def test_last_day_of_last_month(txt_input, expected):
    in_date = datetime.strptime(txt_input, '%Y-%m-%d')
    out_date = datetime.strptime(expected, '%Y-%m-%d').date()
    assert dp.last_day_of_last_month(in_date) == out_date


@pytest.mark.date_test
@pytest.mark.parametrize(
    'txt_input, expected',
    [
        ('2023-01-15', '2023-01-03'),
        ('2022-01-15', '2022-01-03'),
        ('2022-02-15', '2022-02-01'),
        ('2023-04-15', '2023-04-03'),
    ],
)
def test_first_bizday_of_month(txt_input, expected):
    in_date = datetime.strptime(txt_input, '%Y-%m-%d')
    out_date = datetime.strptime(expected, '%Y-%m-%d').date()
    assert dp.first_bizday_of_month(in_date) == out_date


@pytest.mark.date_test
def test_first_day_of_month():
    assert dp.first_day_of_month(datetime(2023, 5, 15)) == date(2023, 5, 1)
    assert dp.first_day_of_month(datetime(2022, 1, 15)) == date(2022, 1, 1)


@pytest.mark.date_test
def test_split_date_token_fmt():
    assert split('abc:YYYY') == ('abc', 'YYYY')
    assert split(' abc : MMdd ') == ('abc', 'MMdd')
    assert split('abc ') == ('today', 'abc')
    assert split(' yyMMdd ') == ('today', 'yyMMdd')
    assert split(' todayPM ') == ('todayPM', 'yyyyMMdd')


@pytest.mark.date_test
def test_parse_format_date():
    assert pf(datetime(2023, 1, 15), 'today', 'yyyyMMdd') == '20230115'
    assert pf(datetime(2023, 1, 15, 19), 'todayPm', 'yyyyMMdd') == '20230114'
    assert pf(datetime(2023, 1, 15, 21), 'todayPm', 'yyyyMMdd') == '20230115'
    assert pf(datetime(2023, 1, 15, 18), 'today', 'yyyyMMdd', 0, -20) == '20230114'
    assert pf(datetime(2023, 1, 3), 'prevWeekDay', 'yyyy-MM-dd') == '2023-01-02'
    assert pf(datetime(2023, 1, 3), 'prevBizDay', 'yyyy-MM-dd') == '2022-12-30'
    assert pf(datetime(2023, 1, 2), 'prevDay', 'yyyy-MM-dd') == '2023-01-01'
    assert pf(datetime(2022, 8, 15), 'lastBizDayOfLastMnth', 'MM/dd/yyyy') == '07/29/2022'
    assert pf(datetime(2022, 8, 15), 'lastDayOfLastMnth', 'yyyy_MM_dd') == '2022_07_31'
    assert pf(datetime(2022, 1, 15), 'firsBizDayOfMnth', 'yyyy_MM_dd') == '2022_01_03'
    assert pf(datetime(2022, 1, 15), 'firsDayOfMnth', 'yyyy_MM_dd') == '2022_01_01'
