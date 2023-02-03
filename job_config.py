import yaml
import logging
from pathlib import Path
from datetime import datetime
import helpers
import commons


class JobConfig:

    def __init__(self, job_name: str, job_config_file_path: str) -> None:
        # Initialize JobConfig by loading the <job_name>.yml into a dictionary

        self.JOB_CONFIG_FILE_PATH = job_config_file_path
        self.job_name: str = job_name

        self.CONFIG_DICT: dict = None
        try:
            with open(self.JOB_CONFIG_FILE_PATH, 'r') as f:
                self.CONFIG_DICT =yaml.safe_load(f)
        except Exception as ex:
            ex.add_note(f'Error reading YAML configuration file: {self.JOB_CONFIG_FILE_PATH}')      
            raise ex  

        self.LOG_FILE_PATH: str = None
        self.force_debug: bool = None
        self.force_env : str = None
        self.log_path: str = None

        self.app_id: str = None
        self.job_description: str = None
        self.use_holiday: bool = None        
        self.watch_file: bool = None
        self.file_name: list = None
        self.file_count: int = None
        self.source_path: str = None
        self.sleep_time: int = None
        self.look_time: int = None
        self.check_age: bool = None
        self.file_age: int = None
        self.copy_file: bool = None
        self.copy_file_name: str = None
        self.copy_path: str = None
        self.archive_file: bool = None
        self.archive_file_name: str = None
        self.archive_path: str = None
        print(f'Configuring logging ... ')
        self.config_logging()
        

    def config_logging(self) -> None:
        # validate log_path from <job_name>.yml, required for logger setup

        # check and set log_path from job config
        self.set_required_key('log_path')
        # check if log_path permission
        if not helpers.is_path_writable(self.log_path):
            raise commons.JobConfigError(f'log_path is not correct or not writable: {self.log_path}')

        # resolve absolute log_file_path
        date_str = datetime.today().strftime("%Y%m%d")
        path = Path(self.log_path).joinpath(f'{self.job_name}_{date_str}.log')
        self.LOG_FILE_PATH = path.resolve() 

        # set up logger 
        #with open(Path(__file__).parent.joinpath('logging.yml'), 'r') as f:
            #config = yaml.safe_load(f.read())
        config = yaml.safe_load(commons.LOGGING_YML)
        print(f'configuring log_path in logger: {self.LOG_FILE_PATH}')
        # overide logger's filename using log_path
        config['handlers']['file']['filename']= self.LOG_FILE_PATH
        logging.config.dictConfig(config)    


    def parse_config(self) -> None:
        # validate all required and optional job variables

        log = logging.getLogger()
        self.set_required_key('app_id')
        self.set_required_key('job_description')
        self.set_flag('use_holiday')
        
        self.set_required_group('watch_file')
        self.set_required_key(key='file_name',group='watch_file')
        self.set_required_key(key='file_count',group='watch_file')
        self.set_required_key(key='source_path',group='watch_file')
        self.set_required_key(key='file_count',group='watch_file')
        self.set_required_key(key='sleep_time',group='watch_file')
        self.set_required_key(key='look_time',group='watch_file')    
        self.set_optional_key(key='min_size',group='watch_file')      
        
        self.set_optional_group('copy_file')
        if self.copy_file:
            self.set_optional_key(key='copy_file_name',group='copy_file')
            self.set_required_key(key='copy_path',group='copy_file')
        
        self.set_optional_group('archive_file')
        if self.archive_file:
            self.set_optional_key(key='archive_file_name',group='archive_file')
            self.set_required_key(key='archive_path',group='archive_file')

    def parse_env_overrides(self) -> None:
        # validate all required and optional job variables
        self.set_environ_overrides()
        #self.check_permission()  

    def set_flag(self,  key: str):
        if key not in self.CONFIG_DICT or not self.CONFIG_DICT[key]:
            setattr(self, key, False)
        else:
            setattr(self, key, self.CONFIG_DICT[key])

    def set_required_group(self,  key: str):
        if key not in self.CONFIG_DICT:
            raise commons.JobConfigError(f'Required group key missing in job config: {key}')
        else:
            setattr(self, key, True)

    def set_optional_group(self,  key: str):
        if key not in self.CONFIG_DICT:
            setattr(self, key, False)  
        else:
            setattr(self, key, True)            

    def set_required_key(self, key: str, group: str = None) -> None:
        if group:
            if key not in self.CONFIG_DICT[group]:
                raise commons.JobConfigError(f'Required key for group <{group}> missing in job config: {key}')
            else:
                if not self.CONFIG_DICT[group][key]:
                    raise commons.JobConfigError(f'Required value for group <{group}> missing in job config: {key}')
                else:
                    setattr(self, key, self.CONFIG_DICT[group][key])
        else:
            if key not in self.CONFIG_DICT:
                raise commons.JobConfigError(f'Required key missing in job config: {key}')
            else:
                if not self.CONFIG_DICT[key]:
                    raise commons.JobConfigError(f'Required value missing in job config: {key}')
                else:
                    setattr(self, key, self.CONFIG_DICT[key])

    def set_optional_key(self, key: str, group: str = None) -> None:
        if group:
            if key in self.CONFIG_DICT[group] and self.CONFIG_DICT[group][key]:
                setattr(self, key, self.CONFIG_DICT[group][key])
        else:
            if key in self.CONFIG_DICT and self.CONFIG_DICT[key]:
                setattr(self, key, self.CONFIG_DICT[key])                    

    def set_environ_overrides(self) -> None:
        if self.force_env and (self.force_env not in self.CONFIG_DICT):
            raise commons.JobConfigError(f'Required env override missing in job config: {self.force_env}')
        elif not self.CONFIG_DICT[self.force_env]:
            raise commons.JobConfigError(f'Env overide is empty in job config: {self.force_env}')
        else:
            for key in self.CONFIG_DICT[self.force_env]:
                if not hasattr(self, key):
                    raise commons.JobConfigError(f'Not defined attribute in job config: {self.force_env} -> {key}') 
                if self.CONFIG_DICT[self.force_env][key]:
                    log = logging.getLogger()
                    log.info(f'Overriding <{key}> from {self.force_env} environment')
                    setattr(self, key, self.CONFIG_DICT[self.force_env][key])      
    
    def check_duplicate(self) -> None:
        if self.copy_file:
            if self.target_s3_uri:
                if self.target_s3_uri == self.source_s3_uri:
                    raise commons.JobConfigError(f'Conflict error: target_s3_uri and source_s3_uri are the same ')
        if self.archive_file:
            if self.archive_s3_uri:
                if (self.archive_s3_uri == self.source_s3_uri) or (self.archive_s3_uri==self.target_s3_uri):
                        raise commons.JobConfigError(f'Conflict error: archive_s3_uri, target_s3_uri, source_s3_uri has to be unique ')       

    def validate_path(self) -> None:
        pass

    def check_permission(self) -> None:
        # check required read/write permission for the job action

        # permission check is optional for source_path as it throws error 
        # right away if permission is missing at beginning of while loop

        # TODO: validate write permission on effective target
        if self.copy_file:
            if self.target_s3_uri:
                if self.target_s3_uri == self.source_s3_uri:
                    raise commons.JobConfigError(f'Conflict error: target_s3_uri and source_s3_uri are the same ')
                # verify s3 custom_errors is writable, cannot find a better way than touching a file
                if not helpers.is_s3_writable(self.copy_s3_bucket, self.copy_s3_prefix):
                    raise commons.JobConfigError(f'target_s3_bucket is not writable: {self.copy_s3_bucket} | {self.copy_s3_prefix}')
            elif self.target_path:
                if not helpers.is_path_writable(self.target_path):
                    raise commons.JobConfigError(f'target_path is not writable: {self.target_path}')
            else:
                raise commons.JobConfigError('Missing config: copy_file = True, however target_path is null ')
        
        # TODO: validate write permission on effective archive 
             
                # verify s3 archive is writable, cannot find a better way than touching a file
            if not helpers.is_s3_writable(self.archive_s3_bucket, self.archive_s3_prefix):
                    raise commons.JobConfigError(f'archive_s3_bucket is not writable: {self.archive_s3_bucket} | {self.archive_s3_prefix}')
            elif self.archive_path:
                if not helpers.is_path_writable(self.archive_path):
                    raise commons.JobConfigError(f'archive_path is not writable: {self.archive_path}')
            else:
                raise commons.JobConfigError('Missing config: archive_file = true, however archive_path is null')


    @property
    def is_source_s3(self):
        if self.source_path:
            if self.source_path.lower().startswith('s3://'):
                return True
            else:
                return False
        else:
            return False

    @property
    def source_s3_bucket(self):
        if self.is_source_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.source_path)
            return bucket
        else:
            return None

    @property
    def source_s3_prefix(self):
        if self.is_source_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.source_path)
            return prefix
        else:
            return None

    @property
    def is_copy_s3(self):
        if self.copy_path:
            if self.copy_path.lower().startswith('s3://'):
                return True
            else:
                return False   
        else:
            return False       

    @property
    def copy_s3_bucket(self):
        if self.is_copy_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.copy_path)
            return bucket
        else:
            return None

    @property
    def copy_s3_prefix(self):
        if self.is_copy_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.copy_path)
            return prefix
        else:
            return None


    @property
    def is_archive_s3(self):
        if self.archive_path:
            if self.archive_path.lower().startswith('s3://'):
                return True
            else:
                return False         
        else:
            return False

    @property
    def archive_s3_bucket(self):
        if self.is_archive_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.archive_path)
            return bucket
        else:
            return None

    @property
    def archive_s3_prefix(self):
        if self.is_archive_s3:
            [bucket, prefix] = helpers.get_s3_bucket_prefix_by_uri(self.archive_path)
            return prefix
        else:
            return None



    def print_config(self) -> None:
        # print all configuration variables using iterator

        log = logging.getLogger()
        log.info('[ Job Config Variables ]')
        log.info( f'{"JOB_CONFIG_FILE_PATH" : <25} : {self.JOB_CONFIG_FILE_PATH }')
        log.info( f'{"LOG_FILE_PATH" : <25} : {self.LOG_FILE_PATH }')
        log.info( f'{"force_debug" : <25} : {self.force_debug }')
        log.info( f'{"force_env" : <25} : {self.force_env }')
        log.info( f'{"log_path" : <25} : {self.log_path }')
        log.info( f'{"job_name" : <25} : {self.job_name }')
        log.info( f'{"app_id" : <25} : {self.app_id }')
        log.info( f'{"job_description" : <25} : {self.job_description }')
        log.info( f'{"use_holiday" : <25} : {self.use_holiday }')        
        log.info( f'{"watch_file" : <25} : {self.watch_file }')
        log.info( f'{"file_name" : <25} : {self.file_name }')
        log.info( f'{"file_count" : <25} : {self.file_count }')
        log.info( f'{"source_path" : <25} : {self.source_path }')
        log.info( f'{"sleep_time" : <25} : {self.sleep_time }')
        log.info( f'{"look_time" : <25} : {self.look_time }')
        log.info( f'{"check_age" : <25} : {self.check_age }')
        log.info( f'{"file_age" : <25} : {self.file_age }')
        log.info( f'{"copy_file" : <25} : {self.copy_file }')
        log.info( f'{"copy_file_name" : <25} : {self.copy_file_name }')
        log.info( f'{"copy_path" : <25} : {self.copy_path }')
        log.info( f'{"archive_file" : <25} : {self.archive_file }')
        log.info( f'{"archive_file_name" : <25} : {self.archive_file_name }')
        log.info( f'{"archive_path" : <25} : {self.archive_path }')
        log.info('[ Resolved Variables ]')
        log.info( f'{"is_source_s3" : <25} : {self.is_source_s3 }')
        log.info( f'{"source_s3_bucket" : <25} : {self.source_s3_bucket }')
        log.info( f'{"source_s3_prefix" : <25} : {self.source_s3_prefix }')
        log.info( f'{"is_copy_s3" : <25} : {self.is_copy_s3 }')
        log.info( f'{"copy_s3_bucket" : <25} : {self.copy_s3_bucket }')
        log.info( f'{"copy_s3_prefix" : <25} : {self.copy_s3_prefix }')
        log.info( f'{"is_archive_s3" : <25} : {self.is_archive_s3 }')
        log.info( f'{"archive_s3_bucket" : <25} : {self.archive_s3_bucket }')
        log.info( f'{"archive_s3_prefix" : <25} : {self.archive_s3_prefix }')


       

