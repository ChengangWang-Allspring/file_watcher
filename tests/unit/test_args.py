import pytest

from file_watch.stage import prepare


@pytest.mark.args_test
def test_valid_db_debug_arguments():
    args = prepare.parse_args(['-m file_watch', '--db', 'agtps', 'test_job', '--debug'])
    assert args.db_profile == 'agtps'
    assert args.debug == True
    assert args.job_name == 'test_job'


@pytest.mark.args_test
def test_valid_non_db_debug_arguments():
    args = prepare.parse_args(['-m file_watch', 'another_job'])
    assert args.db_profile is None
    assert args.debug == False
    assert args.job_name == 'another_job'


@pytest.mark.args_test
def test_invalid_arguments():
    with pytest.raises(SystemExit):
        args = prepare.parse_args(['-m file_watch'])
    with pytest.raises(SystemExit):
        args = prepare.parse_args(['-m file_watch', '--debug'])
    with pytest.raises(SystemExit):
        args = prepare.parse_args(['-m file_watch', '--db', 'db-profile'])
