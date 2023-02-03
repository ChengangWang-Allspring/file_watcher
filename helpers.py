import logging
import random
import traceback
import boto3
import botocore.exceptions
from pathlib import Path
import os


def get_job_config_path(job_name: str) -> Path:
    if "FILE_WATCH_JOB_PATH" in os.environ:
        FILE_WATCH_JOB_PATH = os.environ["FILE_WATCH_JOB_PATH"]
        print(
            f'Using environment variable FILE_WATCH_JOB_PATH for job config: {FILE_WATCH_JOB_PATH}'
        )
    else:
        FILE_WATCH_JOB_PATH = Path.cwd()
        print(f'Using current working directory for job config: {FILE_WATCH_JOB_PATH}')
    path = Path(FILE_WATCH_JOB_PATH)
    return path.joinpath(f"{job_name}.yml")


def get_s3_bucket_prefix_by_uri(url: str) -> list:
    # parse s3 bucket and prefix from the full s3 uri

    url = url.replace("s3://", "")
    bucket = url[: url.index("/")]
    prefix = url[url.index("/") + 1 :]
    return [bucket, prefix]


def get_files_on_s3(my_bucket: str, my_prefix: str) -> list:
    # use boto3 s3 client and function list_objects_v2
    # to retieve list of filenames (without prefix) from s3

    log = logging.getLogger()
    try:
        log.debug("Setting up boto3 s3 client ... ")
        s3 = boto3.client("s3")
        log.debug("Sending request using list_objects_v2 ... ")
        # get AWS response in a dictionary object
        response = s3.list_objects_v2(Bucket=my_bucket, Prefix=my_prefix)
        log.debug("Parsing contents in response ... ")
        if "Contents" in response:
            # get list of file objects by key <Contents>
            contents = response["Contents"]
            # list comprehension to get pure filename list without prefix
            # log.debug(f'Total count in contents including prefix: {len(contents)}')
            # log.debug(contents)
            files = [
                item["Key"].replace(my_prefix, "")
                for item in contents
                if item["Key"] != my_prefix
            ]
            # log.debug(f'Pure filename list (count: {len(files)}) retrieved. ')
            return files
        else:
            log.debug(f"Cannot find <Contents> in response dictionary")
            return []
    except Exception as e:
        e.add_note("Internal Exception thrown during get_files_on_s3.")
        raise e


def is_s3_writable(my_bucket: str, my_prefix: str) -> None:
    # validate write permission on s3 bucket by uploading a touch file

    log = logging.getLogger()
    touch_file_name = "s3_touch.py"
    touch_file_path = Path(__file__).parent.joinpath(touch_file_name)
    touch_key = touch_file_name
    if my_prefix:
        touch_key = f"{my_prefix}{touch_file_name}"
    log.debug(f"touch bucket: {my_bucket}, prefix: {my_prefix}")
    log.debug(f"touch_key: {touch_key}")
    log.debug(f"touch_file_path:  {touch_file_path}")
    s3 = boto3.client("s3")
    try:
        s3.upload_file(touch_file_path, my_bucket, touch_key)
        log.debug("s3 touch-upload seems to complete")
        response = s3.head_object(Bucket=my_bucket, Key=touch_key)
        log.debug("s3 checking if touch file uploaded ...")
        if "ResponseMetadata" in response:
            s3.delete_object(Bucket=my_bucket, Key=touch_key)
        else:
            log.debug(f"s3 touch failure : {my_bucket}{my_prefix}")
        return True
    except botocore.exceptions.ClientError as e:
        log.debug(e)
        return False
    except Exception as e:
        log.debug(e)
        return False


def is_path_writable(my_path: str, filename: str = None) -> bool:
    # validate write permission on path by touch

    log = logging.getLogger()
    if not my_path:
        return False
    try:
        path = Path(my_path)
        log.debug(f"checking if path is writable :{my_path}")
        if not path.is_dir():
            return False
        if not filename:
            filename = str(random.random())[1:]
        path.joinpath(filename)
        log.debug(f"touching a file to checking write permission: {path} ")
        path.touch(exist_ok=True)
        return True

    except Exception as ex:
        log.debug(f"ex")
        log.debug(traceback.format_exc())
        return False
