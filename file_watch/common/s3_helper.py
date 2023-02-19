import boto3

import logging
from datetime import datetime
from typing import Tuple, List, Dict


def get_files_on_s3(
    my_bucket: str, my_prefix: str
) -> Tuple[List[str], Dict[str, datetime], Dict[str, int]]:
    """use boto3 s3 client and function list_objects_v2
    to retieve list of filenames (without prefix) from s3
    """

    log = logging.getLogger()
    try:
        log.debug('Setting up boto3 s3 client ... ')
        s3 = boto3.client('s3')
        log.debug('Sending request using list_objects_v2 ... ')
        # set up paginator to get page by page
        paginator = s3.get_paginator('list_objects_v2')
        PAGE_SIZE = 100
        pages = paginator.paginate(
            Bucket=my_bucket, Prefix=my_prefix, PaginationConfig={'PageSize': PAGE_SIZE}
        )
        obj_list = []
        page_index = 0
        for page in pages:
            if 'Contents' not in page:
                continue
            contents = page['Contents']
            page_index += 1
            log.debug(f'page_index: {page_index }, Files count: {len(contents)}')
            obj_list += page['Contents']
        log.debug(f'total file count in all pages = {len(obj_list)}')

        # list comprehension
        file_names = [
            obj['Key'].replace(my_prefix, '') for obj in obj_list if obj['Key'] != my_prefix
        ]
        # dictionary comprehension
        date_dict = {
            obj['Key'].replace(my_prefix, ''): obj['LastModified']
            for obj in obj_list
            if obj['Key'] != my_prefix
        }
        size_dict = {
            obj['Key'].replace(my_prefix, ''): obj['Size']
            for obj in obj_list
            if obj['Key'] != my_prefix
        }

        return (file_names, date_dict, size_dict)

    except Exception as e:
        e.add_note('Internal Exception thrown during get_files_on_s3.')
        raise e


def get_s3_bucket_prefix_by_uri(url: str) -> List[str]:
    """parse s3 bucket and prefix from s3 uri"""

    url = url.replace('s3://', '')
    bucket = url[: url.index('/')]
    prefix = url[url.index('/') + 1 :]
    return [bucket, prefix]


def copy_files_s3_2_s3(
    source_bucket: str, source_key: str, dest_bucket: str, dest_key: str
) -> None:
    """copy file object from s3 bucket to another s3 bucket"""

    s3 = boto3.resource('s3')
    copy_source = {'Bucket': source_bucket, 'Key': source_key}
    s3.meta.client.copy(copy_source, dest_bucket, dest_key)


def copy_files_s3_2_local(source_bucket: str, source_key: str, dest_file_path: str) -> None:
    """download file object from s3 bucket to local or UNC path"""

    s3 = boto3.resource('s3')
    s3.meta.client.download_file(source_bucket, source_key, dest_file_path)


def copy_files_local_2_s3(source_file_path: str, dest_bucket: str, dest_key: str) -> None:
    """update file object from local or UNC path to s3 bucket"""

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(source_file_path, dest_bucket, dest_key)


def verify_s3_files(file_names: List[str], s3_uri: str) -> bool:
    s3 = boto3.client('s3')
    bucket, prefix = get_s3_bucket_prefix_by_uri(s3_uri)
    for file_name in file_names:
        reponse = s3.list_objects_v2(Bucket=bucket, Prefix=f'{prefix}/{file_name}')
        if len(reponse['Contents']) >= 1:
            continue
        else:
            log = logging.getLogger()
            log.debug(f'file dos not exist in "{s3_uri}": {file_name}')
            return False

    return True
