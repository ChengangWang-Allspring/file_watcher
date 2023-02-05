from pathlib import Path
from datetime import datetime

from file_watch.common import constants
from file_watch.common.settings import Settings


def get_jobs_yml_file_path(job_name: str):
    # get <job_name>.yml absolute path from this module's path
    path = Path(__file__).parent.parent
    path = path.joinpath(Settings.CONFIG_YML_RELATIVE_PATH).joinpath(
        f'{job_name}.yml')
    return path


def get_log_file_path(job_name: str):
    # get logs absolute path from this module's path
    path = Path(__file__).parent.parent
    str_date = datetime.today().strftime('%Y-%m-%d')
    path = path.joinpath(Settings.LOGS_RELATIVE_PATH).joinpath(
        f'{job_name}_{str_date}.log')
    return path


def is_path_valid(my_path: str, filename: str = None) -> bool:

    # consider 3 cases including UNC, local and S3

    pass


if __name__ == '__main__':
    path = get_jobs_yml_file_path('test_job')
    print(path)
