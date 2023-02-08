from pydantic import BaseModel, validator, ValidationError, root_validator

import logging
from typing import Optional, List

from pm_watch.core import core_helper
from pm_watch.helper.common import PathType, JobConfigType, JobConfigError


def list_has_dups(my_list: list) -> bool:
    """convert list to set for dup check excluding None"""

    my_list = [item for item in my_list if item is not None]
    my_set = set(my_list)
    if len(my_set) != len(my_list):
        return True
    else:
        return False


class ValidJobConfig(BaseModel):
    """Validatable job config class using Pydantic"""

    app_id: str
    description: Optional[str]
    file_names: List[str]
    file_count: int
    source_path: str
    sleep_time: int
    look_time: int
    min_size: Optional[int]
    exclude_age: Optional[int]
    use_copy: Optional[bool] = False
    copy_names: Optional[List[str]]
    copy_path: Optional[str]
    use_archive: Optional[bool] = False
    archive_names: Optional[List[str]]
    archive_path: Optional[str]
    offset_days: Optional[int]
    offset_hours: Optional[int]

    # derived fields must be after base fields
    job_name: str = None
    effective_source_path_type: PathType = None
    effective_copy_path_type: PathType = None
    effective_archive_path_type: PathType = None
    effective_file_names: List[str] = None
    effective_job_config_type: JobConfigType = None

    @validator('app_id', always=True)
    @classmethod
    def validate_app_id(cls, value):
        """app_id cannot be empty string"""

        if value is None or value == '':
            raise JobConfigError('app_id cannot be null or empty')
        return value

    @validator('file_names', always=True)
    @classmethod
    def validate_file_names(cls, value):
        """file_names cannot be empty string"""

        # an empty string file_names [''] is a list with one empty string item
        if value is None or len(value) == 0 or len(value[0].strip()) == 0:
            raise JobConfigError('file_names cannot be null or empty')
        return value

    @validator('file_count', always=True)
    @classmethod
    def validate_file_count(cls, value, values):
        """number of files to be expected"""

        if 'file_names' in values and value < len(values['file_names']):
            raise JobConfigError('value must be greater of equal than len of file_names list')
        return value

    @validator('sleep_time', 'look_time', 'exclude_age', always=True)
    @classmethod
    def validate_not_less_than_one(cls, value):
        """these attributes won't accept a zero or negative value"""

        if value is not None and value < 1:
            raise JobConfigError('value must be greater or equal than 1')
        return value

    @validator('copy_path', always=True)
    @classmethod
    def validate_copy_path(cls, value, values):
        """these copy_path is required if use_copy is true"""

        use_copy: bool = values['use_copy'] if 'use_copy' in values else False
        if use_copy and value is None:
            raise JobConfigError('copy_path is required if use_copy is true')
        return value

    @validator('archive_path', always=True)
    @classmethod
    def validate_archive_path(cls, value, values):
        """these archive_path is required if use_archive is true"""

        use_archive: bool = values['use_archive'] if 'use_archive' in values else False
        if use_archive and value is None:
            raise JobConfigError('archive_path is required if use_archive is true')
        return value

    @root_validator
    @classmethod
    def validate_no_dup_source_path(cls, values):
        """business logic validation"""

        # source, copy and archive paths can not be the same
        path_list = [values.get(item) for item in ('source_path', 'copy_path', 'archive_path')]
        if list_has_dups(path_list):
            raise JobConfigError('duplicate values in source_path, copy_path or archive_path')

        # if use_copy true, copy_names should be None or same len as source_name
        use_copy = values.get('use_copy')
        copy_names = values.get('copy_names')
        file_names = values.get('file_names')
        if use_copy and copy_names is not None and len(copy_names) != len(file_names):
            raise JobConfigError('copy_names not the same length as file_names')

        # if use_archive true, archive_names should be None or same len as source_name
        use_archive = values.get('use_archive')
        archive_names = values.get('archive_names')
        file_names = values.get('file_names')
        if use_archive and archive_names is not None and len(archive_names) != len(file_names):
            raise JobConfigError('archive_names not the same length as file_names')

        return values

    @validator('effective_source_path_type', always=True)
    @classmethod
    def validate_effective_source_path_type(cls, value, values, **kwargs):
        """parse path_type, this validator is required for derived fields"""

        source_path = values['source_path']
        path_type: PathType = None
        try:
            path_type = core_helper.validate_path_type(source_path)
        except Exception as ex:
            log = logging.getLogger()
            log.error('Exception caught in validate_effective_source_path_type()')
            raise ex

        if path_type is None:
            raise JobConfigError('cannot derive source_path_type from source_path')

        return path_type

    @validator('effective_copy_path_type', always=True)
    @classmethod
    def validate_effective_copy_path_type(cls, value, values, **kwargs):
        """parse path_type, this validator is required for derived fields"""

        use_copy = values['use_copy'] if 'use_copy' in values else False
        copy_path = values['copy_path'] if 'copy_path' in values else ''
        path_type: PathType = None
        if use_copy:
            try:
                path_type = core_helper.validate_path_type(copy_path)
            except Exception as ex:
                log = logging.getLogger()
                log.error('Excetion caught in validate_effective_copy_path_type()')
                raise ex
            if path_type is None:
                raise JobConfigError('cannot derive effective_copy_path_type from copy_path')
        return path_type

    @validator('effective_archive_path_type', always=True)
    @classmethod
    def validate_effective_archive_path_type(cls, value, values, **kwargs):
        """parse path_type, this validator is required for derived fields"""

        use_archive = values['use_archive'] if 'use_archive' in values else False
        archive_path = values['archive_path'] if 'archive_path' in values else False
        path_type: PathType = None
        if use_archive:
            try:
                path_type = core_helper.validate_path_type(archive_path)
            except Exception as ex:
                log = logging.getLogger()
                log.error('Exception caught in validate_effective_archive_path_type()')
                raise ex
            if path_type is None:
                raise JobConfigError('cannot derive effective_archive_path_type from archive_path')

        return path_type

    @validator('effective_file_names', always=True)
    @classmethod
    def validate_effective_file_names(cls, value, values, **kwargs):
        """parse list of file_names with date token and date format in it
        return values will be saved in effective_file_names
        """
        offset_days = values['offset_days'] if 'offset_days' in values else None
        offset_hours = values['offset_hours'] if 'offset_hours' in values else None
        file_names = values['file_names'] if 'file_names' in values else None
        eff_file_names = None
        if file_names is not None:
            try:
                eff_file_names = [
                    core_helper.parse_file_name(item, offset_days, offset_hours)
                    for item in file_names
                ]
            except Exception as ex:
                log = logging.getLogger()
                log.error('Exception caught in validate_effective_file_names()')
                raise ex

        if eff_file_names is None or len(file_names[0].strip()) == 0:
            raise JobConfigError('cannot derive effective_file_names from file_names')
        return eff_file_names

    def print_log(self):
        log = logging.getLogger()
        log.info('<< Job Config Variables >>')
        log.info(f'{"app_id"} : {self.app_id }')
        log.info(f'{"description"} : {self.description }')
        log.info(f'{"file_names"} : {self.file_names }')
        log.info(f'{"file_count"} : {self.file_count }')
        log.info(f'{"source_path"} : {self.source_path }')
        log.info(f'{"sleep_time"} : {self.sleep_time }')
        log.info(f'{"look_time"} : {self.look_time }')
        log.info(f'{"min_size"} : {self.min_size }')
        log.info(f'{"exclude_age"} : {self.exclude_age }')
        log.info(f'{"use_copy"} : {self.use_copy }')
        log.info(f'{"copy_names"} : {self.copy_names }')
        log.info(f'{"copy_path"} : {self.copy_path }')
        log.info(f'{"use_archive"} : {self.use_archive }')
        log.info(f'{"archive_names"} : {self.archive_names }')
        log.info(f'{"archive_path"} : {self.archive_path }')
        log.info(f'{"offset_days"} : {self.offset_days }')
        log.info(f'{"offset_hours"} : {self.offset_hours }')
        log.info('<< Resolved Variables >>')
        log.info(f'{"effective_source_path_type"} : {self.effective_source_path_type }')
        log.info(f'{"effective_copy_path_type"} : {self.effective_copy_path_type }')
        log.info(f'{"effective_archive_path_type"} : {self.effective_archive_path_type }')
        log.info(f'{"effective_file_names"} : {self.effective_file_names }')
        log.info(f'{"effective_job_config_type"} : {self.effective_job_config_type }')
