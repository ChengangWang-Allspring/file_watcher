from pydantic import BaseModel, validator, ValidationError, root_validator

import logging
from typing import Optional, List

from pm_watch.core import config_parser
from pm_watch.helper.common import PathType, JobConfigType


def list_has_dups(my_list: list) -> bool:
    """ convert list to set for dup check excluding None """

    my_list = [item for item in my_list if item is not None]
    my_set = set(my_list)
    if len(my_set) != len(my_list):
        return True
    else:
        return False


class ValidJobConfig(BaseModel):
    """ Validatable job config class using Pydantic """

    app_id: str
    description: Optional[str]
    file_name: List[str]
    file_count: int
    source_path: str
    sleep_time: int
    look_time: int
    min_size: Optional[int]
    exclude_age: Optional[int]
    use_copy: Optional[bool] = False
    copy_name: Optional[List[str]]
    copy_path: Optional[str]
    use_archive: Optional[bool] = False
    archive_name: Optional[List[str]]
    archive_path: Optional[str]
    offset_days: Optional[int]
    offset_hours: Optional[int]

    # derived fields must be after base fields
    job_name: str = None
    effective_source_path_type: PathType = None
    effective_copy_path_type: PathType = None
    effective_archive_path_type: PathType = None
    effective_file_name: List[str] = None
    effective_job_config_type: JobConfigType = None

    @validator('file_count')
    @classmethod
    def validate_file_count(cls, value, values):
        """ number of files to be expected """

        if 'file_name' in values and value < len(values['file_name']):
            raise ValueError(
                'value must be greater of equal than len of file_name list'
            )
        return value

    @validator('sleep_time', 'look_time', 'exclude_age')
    @classmethod
    def validate_not_less_than_one(cls, value):
        """ these attributes won't accept a zero or negative value """

        if value < 1:
            raise ValueError('value must be greater or equal than 1')
        return value

    @validator('copy_path', always=True)
    @classmethod
    def validate_copy_path(cls, value, values):
        """ these copy_path is required if use_copy is true """

        if 'use_copy' in values and values['use_copy'] and value is None:
            raise ValueError(
                'copy_path is required if use_copy is true'
            )
        return value

    @validator('archive_path', always=True)
    @classmethod
    def validate_archive_path(cls, value, values):
        """ these archive_path is required if use_archive is true """

        if 'archive_path' in values and values['archive_path'] and value is None:
            raise ValueError(
                'archive_path is required if use_archive is true'
            )
        return value

    @root_validator
    @classmethod
    def validate_no_dup_source_path(cls, values):
        """ business logic validation """

        # source, copy and archive paths can not be the same
        path_list = [values.get(item) for item in ('source_path', 'copy_path', 'archive_path')]
        if list_has_dups(path_list):
            raise ValueError('duplicate values in source_path, copy_path or archive_path')

        # if use_copy true, copy_name should be null or same len as source_name
        use_copy, copy_name, file_name = values.get('use_copy'), values.get('copy_name'), values.get('file_name')
        if use_copy and copy_name:
            if len(copy_name) != len(file_name):
                raise ValueError('copy_name not the same length as file_name')

        # if use_archive true, archive_name should be null or same len as source_name
        use_archive, archive_name, file_name = values.get('use_archive'), values.get('archive_name'), values.get('file_name')
        if use_archive and archive_name is not None:
            if len(archive_name) != len(file_name):
                raise ValueError('archive_name not the same length as file_name')
        return values

    @validator('effective_source_path_type', always=True)
    @classmethod
    def validate_effective_source_path_type(cls, value, values, **kwargs):
        """ parse path_type, this validator is required for derived fields """

        print('source_path' in values)
        source_path = values['source_path']
        print(f'source_path: {source_path}')
        # no need to check None as it's checked in source_path validator
        try:
            result = config_parser.validate_path_type(source_path)
            return result
        except Exception as ex:
            log = logging.getLogger()
            log.error('Exception caught in effective_source_path_type')

        return None

    @validator('effective_copy_path_type', always=True)
    @classmethod
    def validate_effective_copy_path_type(cls, value, values, **kwargs):
        """ parse path_type, this validator is required for derived fields """

        copy_path = values['copy_path']
        if copy_path != None:
            try:
                result = config_parser.validate_path_type(copy_path)
                return result
            except Exception as ex:
                log = logging.getLogger()
                log.error('Excetion caught in effective_copy_path_type')
                raise ex
        else:
            return None

    @validator('effective_archive_path_type', always=True)
    @classmethod
    def validate_effective_archive_path_type(cls, value, values, **kwargs):
        """ parse path_type, this validator is required for derived fields """

        archive_path = values['archive_path']
        print(f'archive_path is: {archive_path}')
        if archive_path != None:
            try:
                result = config_parser.validate_path_type(archive_path)
                return result
            except Exception as ex:
                log = logging.getLogger()
                log.error('Exception caught in effective_archive_path_type')
                raise ex
        else:
            return None

    @validator('effective_file_name', always=True)
    @classmethod
    def validate_effective_file_name(cls, value, values, **kwargs):
        """ parse list of file_name with date token and date format in it 
            return values will be saved in effective_file_name 
        """
        offset_days = values['offset_days']
        offset_hours = values['offset_hours']
        return [config_parser.parse_file_name(item, offset_days, offset_hours) for item in values['file_name']]

    def print_log(self):
        log = logging.getLogger()
        log.info('<< Job Config Variables >>')
        log.info(f'{"app_id"} : {self.app_id }')
        log.info(f'{"description"} : {self.description }')
        log.info(f'{"file_name"} : {self.file_name }')
        log.info(f'{"file_count"} : {self.file_count }')
        log.info(f'{"source_path"} : {self.source_path }')
        log.info(f'{"sleep_time"} : {self.sleep_time }')
        log.info(f'{"look_time"} : {self.look_time }')
        log.info(f'{"min_size"} : {self.min_size }')
        log.info(f'{"exclude_age"} : {self.exclude_age }')
        log.info(f'{"use_copy"} : {self.use_copy }')
        log.info(f'{"copy_name"} : {self.copy_name }')
        log.info(f'{"copy_path"} : {self.copy_path }')
        log.info(f'{"use_archive"} : {self.use_archive }')
        log.info(f'{"archive_name"} : {self.archive_name }')
        log.info(f'{"archive_path"} : {self.archive_path }')
        log.info(f'{"offset_days"} : {self.offset_days }')
        log.info(f'{"offset_hours"} : {self.offset_hours }')
        log.info('<< Resolved Variables >>')
        log.info(f'{"effective_source_path_type"} : {self.effective_source_path_type }')
        log.info(f'{"effective_copy_path_type"} : {self.effective_copy_path_type }')
        log.info(f'{"effective_archive_path_type"} : {self.effective_archive_path_type }')
        log.info(f'{"effective_file_name"} : {self.effective_file_name }')
        log.info(f'{"effective_job_config_type"} : {self.effective_job_config_type }')
