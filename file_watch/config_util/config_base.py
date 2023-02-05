from abc import ABC, abstractmethod


class ConfigBase(ABC):

    def __init__(self, job_name: str):
        self.job_name = job_name

    @abstractmethod
    def get_config_dict(self) -> dict:
        pass
