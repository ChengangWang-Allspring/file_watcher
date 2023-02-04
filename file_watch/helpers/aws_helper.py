import boto3
import botocore.exceptions

import logging


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


def get_s3_bucket_prefix_by_uri(url: str) -> list:
    # parse s3 bucket and prefix from the full s3 uri

    url = url.replace("s3://", "")
    bucket = url[: url.index("/")]
    prefix = url[url.index("/") + 1:]
    return [bucket, prefix]
