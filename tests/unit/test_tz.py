import pytest
import pytz
from tzlocal import get_localzone

from datetime import datetime, timedelta

from file_watch.common import tz_helper


@pytest.mark.tz_test
def test_has_tz():
    assert tz_helper.has_tz(datetime.now()) == False
    assert tz_helper.has_tz(datetime.utcnow().replace(tzinfo=pytz.UTC)) == True
    assert tz_helper.has_tz(datetime.utcnow().replace(tzinfo=get_localzone())) == True


@pytest.mark.tz_test
def test_replace_tz_local():
    now = datetime.now()
    my_date = now.replace(tzinfo=get_localzone())
    assert my_date == tz_helper.replace_tz_local(my_date)
    assert now.strftime('%Y-%m-%d %H:%M:%S.%f') == my_date.strftime('%Y-%m-%d %H:%M:%S.%f')


@pytest.mark.tz_test
def test_replace_tz_utc():
    now = datetime.now()
    my_date = now.replace(tzinfo=pytz.UTC)
    assert my_date == tz_helper.replace_tz_utc(my_date)
    assert now.strftime('%Y-%m-%d %H:%M:%S.%f') == my_date.strftime('%Y-%m-%d %H:%M:%S.%f')


@pytest.mark.tz_test
def test_remove_tz():
    now = datetime.now()
    my_date = now.replace(tzinfo=pytz.UTC)
    assert tz_helper.has_tz(tz_helper.remove_tz(my_date)) == False
    assert now.strftime('%Y-%m-%d %H:%M:%S.%f') == my_date.strftime('%Y-%m-%d %H:%M:%S.%f')


@pytest.mark.tz_test
def test_utc_to_local():
    # my local timezone is Eastern (new york)
    my_utc_date = datetime.now().replace(tzinfo=pytz.UTC)
    my_local_date = tz_helper.utc_to_local(my_utc_date)
    diff: timedelta = my_utc_date - my_local_date
    assert diff.seconds == 0  # my local timezone is Eastern (new york)


@pytest.mark.tz_test
def test_local_to_utc():
    local_timezone = get_localzone()
    # my local timezone is Eastern (new york)
    my_local_date = datetime.now().replace(tzinfo=local_timezone)
    my_utc_date = tz_helper.local_to_utc(my_local_date)
    diff: timedelta = my_utc_date - my_local_date
    assert diff.seconds == 0  # my local timezone is Eastern (new york)
