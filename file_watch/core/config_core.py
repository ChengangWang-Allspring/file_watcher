from pydantic import BaseModel, validator, root_validator

import logging
from typing import Optional, List, Any

from file_watch.core import core_helper
from file_watch.common.enum_const import PathType


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

    job_name: str
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
    target_path: Optional[str]
    use_archive: Optional[bool] = False
    archive_names: Optional[List[str]]
    archive_path: Optional[str]
    offset_days: Optional[int]
    offset_hours: Optional[int]

    # derived fields must be after base fields
    effective_source_path_type: PathType = PathType.NONE
    effective_target_path_type: PathType = PathType.NONE
    effective_archive_path_type: PathType = PathType.NONE
    effective_file_names: Optional[List[str]] = None

    @validator('app_id', always=True)
    @classmethod
    def validate_app_id(cls, value: Any) -> Any:
        """app_id cannot be empty string"""

        if value is None or value == '':
            raise ValueError('app_id cannot be null or empty')
        return value

    @validator('file_names', always=True)
    @classmethod
    def validate_file_names(cls, value: Any) -> Any:
        """file_names cannot be empty string"""

        # an empty string file_names [''] is invalid
        if value is None or len(value) == 0 or len(value[0].strip()) == 0:
            raise ValueError('file_names cannot be null or empty')
        return value

    @validator('file_count', always=True)
    @classmethod
    def validate_file_count(cls, value: Any, values: Any) -> Any:
        """number of files to be expected"""

        file_names = values.get('file_names')
        if file_names is not None and value < len(file_names):
            raise ValueError('value must be greater of equal than len of file_names list')
        return value

    @validator('sleep_time', 'look_time', always=True)
    @classmethod
    def validate_mandatory_int(cls, value: Any) -> Any:
        """these attributes won't accept a zero or negative value"""

        if value is not None and value < 1:
            raise ValueError('value must be greater or equal than 1')
        return value

    @validator('min_size', 'exclude_age')
    @classmethod
    def validate_optional_int(cls, value: Any) -> Any:
        """min_size cannot be less than 1"""

        if value is not None and value < 1:
            raise ValueError('value must be greater or equal than 1')
        return value

    @validator('target_path', always=True)
    @classmethod
    def validate_target_path(cls, value: Any, values: dict) -> Any:
        """these target_path is required if use_copy is true"""

        use_copy: bool = values.get('use_copy', False)
        if use_copy and value is None:
            raise ValueError('target_path is required if use_copy is true')
        return value

    @validator('archive_path', always=True)
    @classmethod
    def validate_archive_path(cls, value: Any, values: dict) -> Any:
        """these archive_path is required if use_archive is true"""

        use_archive: bool = values.get('use_archive', False)
        if use_archive and value is None:
            raise ValueError('archive_path is required if use_archive is true')
        return value

    @root_validator
    @classmethod
    def validate_no_dup_source_path(cls, values: dict) -> dict:
        """business logic validation"""

        # source, copy and archive paths can not be the same
        path_list = [values.get(item) for item in ('source_path', 'target_path', 'archive_path')]
        if list_has_dups(path_list):
            raise ValueError('duplicate values in source_path, target_path or archive_path')

        file_names = values.get('file_names')
        # if use_copy true, copy_names should be None or same len as source_name
        use_copy: bool = values.get('use_copy')
        copy_names: List[str] = values.get('copy_names')
        if use_copy and copy_names is not None and len(copy_names) != len(file_names):
            raise ValueError('copy_names not the same length as file_names')

        # if use_archive true, archive_names should be None or same len as source_name
        use_archive: bool = values.get('use_archive')
        archive_names: List[str] = values.get('archive_names')
        if use_archive and archive_names is not None and len(archive_names) != len(file_names):
            raise ValueError('archive_names not the same length as file_names')

        return values

    @root_validator
    @classmethod
    def validate_effective_source_path_type(cls, values: dict) -> dict:
        """parse path_type, this validator is required for derived fields"""

        source_path: str = values.get('source_path')
        path_type: PathType = core_helper.validate_path_type(source_path)
        if path_type == PathType.NONE:
            raise ValueError('cannot derive effective_source_path_type from source_path')

        values['effective_source_path_type'] = path_type
        return values

    @root_validator
    @classmethod
    def validate_effective_target_path_type(cls, values: dict) -> dict:
        """parse path_type, this validator is required for derived fields"""

        use_copy: bool = values.get('use_copy', False)
        target_path: str = values.get('target_path', None)
        path_type: PathType = PathType.NONE
        if use_copy:
            path_type = core_helper.validate_path_type(target_path)
            if path_type == PathType.NONE:
                raise ValueError('cannot derive effective_target_path_type from target_path')

        values['effective_target_path_type'] = path_type
        return values

    @root_validator
    @classmethod
    def validate_effective_archive_path_type(cls, values: dict) -> dict:
        """parse path_type, this validator is required for derived fields"""

        use_archive = values.get('use_archive', False)
        archive_path = values.get('archive_path')
        path_type = PathType.NONE
        if use_archive:
            path_type = core_helper.validate_path_type(archive_path)
            if path_type == PathType.NONE:
                raise ValueError('cannot derive effective_archive_path_type from archive_path')
        values['effective_archive_path_type'] = path_type
        return values

    @root_validator
    @classmethod
    def validate_effective_file_names(cls, values: dict) -> dict:
        """parse list of file_names with date token and date format in it
        return values will be saved in effective_file_names
        """

        offset_days = values.get('offset_days')
        offset_hours = values.get('offset_hours')
        file_names = values.get('file_names')
        eff_file_names = None
        if file_names is not None:
            try:
                eff_file_names = [
                    core_helper.parse_file_name(item, offset_days, offset_hours)
                    for item in file_names
                ]
                log = logging.getLogger()
                log.info('-' * 80)
            except Exception as ex:
                log = logging.getLogger()
                log.error('Exception caught in validate_effective_file_names()')
                raise ex

        if eff_file_names is None or len(file_names[0].strip()) == 0:
            raise ValueError('cannot derive effective_file_names from file_names')

        values['effective_file_names'] = eff_file_names
        return values

    def print_all_variables(self) -> None:
        log = logging.getLogger()
        log.info('<< Job Config Variables >>')
        log.info(f'{"job_name"} : {self.job_name }')
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
        log.info(f'{"target_path"} : {self.target_path }')
        log.info(f'{"use_archive"} : {self.use_archive }')
        log.info(f'{"archive_names"} : {self.archive_names }')
        log.info(f'{"archive_path"} : {self.archive_path }')
        log.info(f'{"offset_days"} : {self.offset_days }')
        log.info(f'{"offset_hours"} : {self.offset_hours }')
        log.info('-' * 80)
        log.info('<< Resolved Variables >>')
        log.info(f'{"effective_source_path_type"} : {self.effective_source_path_type }')
        log.info(f'{"effective_target_path_type"} : {self.effective_target_path_type }')
        log.info(f'{"effective_archive_path_type"} : {self.effective_archive_path_type }')
        log.info(f'{"effective_file_names"} : {self.effective_file_names }')
        log.info('-' * 80)
