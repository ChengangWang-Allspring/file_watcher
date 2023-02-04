from pydantic import BaseModel, validator, ValidationError, root_validator
from typing import Optional, List

from file_watch.helpers import path_helper, valid_helper, file_name_helper


class ValidJobConfig(BaseModel):
    app_id: str
    description: Optional[str]
    use_holiday: bool = True
    use_watch: bool = True
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
    use_archive: Optional[bool]
    archive_name: Optional[List[str]]
    archive_path: str = False

    # derived fields must be after base fields
    source_path_type: str = None
    effective_file_name: str = None

    @validator('use_watch')
    def validate_use_watch(cls, value):
        if not value:
            raise ValueError('value must be true')
        return value

    @validator('file_count')
    def validate_file_count(cls, value, values):
        if 'file_name' in values and value < len(values['file_name']):
            raise ValueError(
                'value must be greater of equal than len of file_name list'
            )
        return value

    @validator('sleep_time', 'look_time', 'exclude_age')
    def validate_not_less_than_one(cls, value):
        if value < 1:
            raise ValueError('value must be greater or equal than 1')
        return value

    @root_validator
    def validate_no_dup_source_path(cls, values):
        # more complex validation logic
        # source, copy and archive paths can not be the same
        path_list = [values.get(item) for item in ('source_path', 'copy_path', 'archive_path')]
        if valid_helper.has_dups_exclude_none(path_list):
            raise ValueError('duplicate values in source_path, copy_path or archive_path')
        # if use_copy true, copy_name should be null or same len as source_name
        use_copy, copy_name, file_name = values.get('use_copy'), values.get('copy_name'), values.get('file_name')
        if use_copy and copy_name:
            if len(copy_name) != len(file_name):
                raise ValueError('copy_name not the same lenght as file_name')

        # if use_archive true, archive_name should be null or same len as source_name
        use_archive, archive_name, file_name = values.get('use_archive'), values.get('archive_name'), values.get('file_name')
        if use_archive and archive_name is not None:
            if len(archive_name) != len(file_name):
                raise ValueError('archive_name not the same length as file_name')
        return values

    @validator('source_path_type', always=True)
    def validate_source_path_type(cls, value, values, **kwargs):
        source_path = values['source_path']
        if source_path.lower().startswith('s3://'):
            return 'S3'
        else:
            return 'Not S3'

    @validator('effective_file_name', always=True)
    def validate_effective_file_name(cls, value, values, **kwargs):
        return [file_name_helper.parse_file_name(item) for item in values['file_name']]
