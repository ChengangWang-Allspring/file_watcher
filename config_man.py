from job_config import JobConfig
import commons


class ConfigManager: 
    my_config: JobConfig = None    

    @classmethod
    def get_config(cls, job_name: str = None,  job_config_file_path: str = None) -> JobConfig:
        # get the single global instance of JobConfig from here

        if cls.my_config:
            return cls.my_config
        elif not job_config_file_path:
            raise commons.JobConfigError('job config file path is missing')
        else:
            cls.my_config = JobConfig(job_name, job_config_file_path)
            return cls.my_config

    