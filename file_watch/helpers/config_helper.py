import yaml

from file_watch.helpers import path_helper

# read config from configuration source


def read_csv_config(job_name: str) -> dict:
    pass


def read_yml_config(job_name: str) -> dict:

    try:
        yml_config_path = path_helper.get_jobs_yml_file_path(job_name)
        with open(yml_config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return config_dict
    except Exception as ex:
        ex.add_note(f'Error reading job config yml file: {yml_config_path}')
        raise ex


def read_db_config(job_name: str) -> dict:
    pass
