import pytest

from file_watch.core.config_core import ValidJobConfig


@pytest.fixture
def input_job_dict():
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
def test_valid_config_1(input_job_dict):
    # with pytest.raises(ValueError):
    _ = ValidJobConfig(**input_job_dict)


@pytest.mark.config_test
def test_bad_file_name_1(input_job_dict):
    """invalid empty file_names string"""
    with pytest.raises(ValueError):
        input_job_dict['file_names'] = ['']
        _ = ValidJobConfig(**input_job_dict)


@pytest.mark.config_test
def test_bad_file_name_2(input_job_dict):
    """invalid null file_name string"""

    with pytest.raises(ValueError):
        input_job_dict['file_names'] = None
        _ = ValidJobConfig(**input_job_dict)


@pytest.mark.config_test
def test_bad_file_name_3(input_job_dict):
    """invalid date token or format"""

    # with pytest.raises(ValueError):
    input_job_dict['file_names'] = ['test{aasdfadsf}_.txt']
    _ = ValidJobConfig(**input_job_dict)
