import pytest
from datetime import date, datetime, time

from file_watch.core import date_parser as dp
from file_watch.core.date_parser import cnv_csharp_date_fmt as cnv_fmt
from file_watch.core.date_parser import datetime_offset as offset
from file_watch.core.date_parser import split_date_token_fmt as split
from file_watch.core.date_parser import parse_format_date as pf


@pytest.mark.date
def test_cnv_csharp_date_fmt():
    assert cnv_fmt('yyyyMMdd') == '%Y%m%d'
    assert cnv_fmt('yyyy-MM-dd') == '%Y-%m-%d'
    assert cnv_fmt('MM/dd/yyyy') == '%m/%d/%Y'
    assert cnv_fmt('MMddyyyy') == '%m%d%Y'
    assert cnv_fmt('yyMMdd') == '%y%m%d'
    assert cnv_fmt('yyyy_MM_dd') == '%Y_%m_%d'


@pytest.mark.date
def test_dattime_offset():
    assert offset(datetime(2023, 1, 15, 12, 30, 00), -2, -6) == datetime(2023, 1, 13, 6, 30, 00)


@pytest.mark.date
def test_today():
    assert dp.today(datetime(2023, 1, 3)) == date(2023, 1, 3)


@pytest.mark.date
def test_today_pm():
    assert dp.today_pm(datetime(2023, 1, 17, 19)) == date(2023, 1, 16)
    assert dp.today_pm(datetime(2023, 1, 17, 21)) == date(2023, 1, 17)


@pytest.mark.date
def test_prev_weekday():
    assert dp.prev_weekday(datetime(2023, 1, 2)) == date(2022, 12, 30)
    assert dp.prev_weekday(datetime(2023, 1, 3)) == date(2023, 1, 2)
    assert dp.prev_weekday(datetime(2023, 1, 1)) == date(2022, 12, 30)
    assert dp.prev_weekday(datetime(2022, 12, 31)) == date(2022, 12, 30)
    assert dp.prev_weekday(datetime(2022, 12, 30)) == date(2022, 12, 29)


@pytest.mark.date
def test_prev_day():
    assert dp.prev_weekday(datetime(2023, 1, 3)) == date(2023, 1, 2)


@pytest.mark.date
def test_prev_bizday():
    assert dp.prev_bizday(datetime(2023, 11, 13)) == date(2023, 11, 9)
    assert dp.prev_bizday(datetime(2023, 11, 12)) == date(2023, 11, 9)
    assert dp.prev_bizday(datetime(2023, 11, 11)) == date(2023, 11, 9)
    assert dp.prev_bizday(datetime(2023, 11, 10)) == date(2023, 11, 9)
    assert dp.prev_bizday(datetime(2023, 11, 14)) == date(2023, 11, 13)
    assert dp.prev_bizday(datetime(2022, 5, 31)) == date(2022, 5, 27)


@pytest.mark.date
def test_last_bizday_of_last_month():
    assert dp.last_bizday_of_last_month(datetime(2022, 8, 15)) == date(2022, 7, 29)
    assert dp.last_bizday_of_last_month(datetime(2022, 7, 15)) == date(2022, 6, 30)
    assert dp.last_bizday_of_last_month(datetime(2022, 3, 15)) == date(2022, 2, 28)
    assert dp.last_bizday_of_last_month(datetime(2021, 6, 15)) == date(2021, 5, 28)


@pytest.mark.date
def test_last_day_of_last_month():
    assert dp.last_day_of_last_month(datetime(2022, 7, 15)) == date(2022, 6, 30)
    assert dp.last_day_of_last_month(datetime(2021, 6, 15)) == date(2021, 5, 31)
    assert dp.last_day_of_last_month(datetime(2022, 3, 15)) == date(2022, 2, 28)


@pytest.mark.date
def test_first_bizday_of_month():
    assert dp.first_bizday_of_month(datetime(2023, 1, 15)) == date(2023, 1, 3)
    assert dp.first_bizday_of_month(datetime(2022, 1, 15)) == date(2022, 1, 3)
    assert dp.first_bizday_of_month(datetime(2022, 2, 15)) == date(2022, 2, 1)
    assert dp.first_bizday_of_month(datetime(2023, 4, 15)) == date(2023, 4, 3)


@pytest.mark.date
def test_first_day_of_month():
    assert dp.first_day_of_month(datetime(2023, 5, 15)) == date(2023, 5, 1)
    assert dp.first_day_of_month(datetime(2022, 1, 15)) == date(2022, 1, 1)


@pytest.mark.date
def test_split_date_token_fmt():
    assert split('abc:YYYY') == ('abc', 'YYYY')
    assert split(' abc : MMdd ') == ('abc', 'MMdd')
    assert split('abc ') == ('today', 'abc')
    assert split(' yyMMdd ') == ('today', 'yyMMdd')
    assert split(' todayPM ') == ('todayPM', 'yyyyMMdd')


@pytest.mark.date
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
