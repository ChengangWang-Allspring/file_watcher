import pytest

from file_watch.core.config_core import ValidJobConfig


@pytest.fixture
def job_dict():
    job_dict: dict = {
        'job_name': 'test_1',
        'app_id': 'TEST',
        'job_description': 'Test job for PyTest',
        'file_names': ['Test_{yyyyMMdd}.dat'],
        'file_count': 1,
        'source_path': r'C:\cwang\Apps\inbound',
        'sleep_time': 3,
        'look_time': 10,
    }
    yield job_dict


@pytest.mark.config_test
def test_valid_config(job_dict):
    """valid job dict"""
    _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_file_name_1(job_dict):
    with pytest.raises(ValueError):
        job_dict['file_names'] = ['']
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_file_name_2(job_dict):
    with pytest.raises(ValueError):
        job_dict['file_names'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_source_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['source_path'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_sleep_time(job_dict):
    with pytest.raises(ValueError):
        job_dict['sleep_time'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_look_time(job_dict):
    with pytest.raises(ValueError):
        job_dict['look_time'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_date_token(job_dict):
    with pytest.raises(ValueError):
        job_dict['file_names'] = ['test{asdfafd:yyMMdd}_.txt']
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_too_many_date_token(job_dict):
    with pytest.raises(ValueError):
        job_dict['file_names'] = ['test{today:yyMMdd}_test{today:MMddyyyy}.txt']
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_app_id(job_dict):
    with pytest.raises(ValueError):
        job_dict['app_id'] = ''
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_file_count_1(job_dict):
    with pytest.raises(ValueError):
        job_dict['file_names'] = ['a', 'b']
        job_dict['file_count'] = 1
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_sleep_time(job_dict):
    with pytest.raises(ValueError):
        job_dict['sleep_time'] = 0
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_look_time(job_dict):
    with pytest.raises(ValueError):
        job_dict['look_time'] = 0
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_exclude_age(job_dict):
    with pytest.raises(ValueError):
        job_dict['exclude_age'] = 0
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_target_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['use_copy'] = True
        job_dict['target_path'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_target_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['use_copy'] = True
        job_dict['target_path'] = 'adf:\\123123'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_missing_archive_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['use_archive'] = True
        job_dict['archive_path'] = None
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_archive_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['use_archive'] = True
        job_dict['archive_path'] = 'adf:\\123123'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_dup_path_1(job_dict):
    with pytest.raises(ValueError):
        job_dict['source_path'] = r'c:\temp\inbound'
        job_dict['target_path'] = r'c:\temp\inbound'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_dup_path_2(job_dict):
    with pytest.raises(ValueError):
        job_dict['source_path'] = r'c:\temp\inbound'
        job_dict['archive_path'] = r'c:\temp\inbound'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_dup_path_3(job_dict):
    with pytest.raises(ValueError):
        job_dict['target_path'] = r'c:\temp\inbound'
        job_dict['archive_path'] = r'c:\temp\inbound'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_source_path(job_dict):
    with pytest.raises(ValueError):
        job_dict['source_path'] = 'adf:\\123123'
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_min_size(job_dict):
    with pytest.raises(ValueError):
        job_dict['min_size'] = -5
        _ = ValidJobConfig(**job_dict)


@pytest.mark.config_test
def test_bad_exclude_age(job_dict):
    with pytest.raises(ValueError):
        job_dict['exclude_age'] = -5
        _ = ValidJobConfig(**job_dict)
