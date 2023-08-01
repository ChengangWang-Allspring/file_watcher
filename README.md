# File Watcher CLI Application

A file watcher application build in Python, as a supplement for the Autosys workload scheduling. 

## Description

The file watcher is for watching, validating and transferring one or multiple files from a source location (S3 bucket or network share), to application inbound folder on EC2 server. The current build is only tested in Windows Server. 

## Getting Started

 See the installation guide below.

### Dependencies

* Python 3.11
* ex. Windows 10
* use ```pip install -r requirements.txt``` to install 3rd parth packages in a Python virtual environment

### File Watcher App - EC2 Windows Installation Guide

* How/where to download the app
https://github.com/ChengangWang-Allspring/file_watcher

* steps to install the app on EC2 (d:\ drive on EC2 windows server)
1. install Python 3.11
2. Set up a virtual environment using installed version of Python 3.11: d:\Apps\common\python_venv\venv_311_pm_watch
using the following command as an example
`python -m venv D:\Apps\common\python_venv\venv_311_pm_watch`
3. Setup system environment variable: PYTHON_VENV  =  D:\Apps\common\python_venv\venv_311_pm_watch\Scripts\python.exe
4. Setup another system environment variable: PYTHONPATH = D:\Apps\common
4. xcopy the whole folder `file_watch` from `file_watcher` (file_watcher is the root of the project) to D:\Apps\common
5. Use the following command in the Autosys File_Watch job
command = ```%PYTHON_VENV% -m file_watch %AUTO_JOB_NAME%```
Standard output file = >D:\Apps\Logs\%AUTO_JOB_NAME%_%AUTORUN%.out
Standard error file = >D:\Apps\Logs\%AUTO_JOB_NAME%_%AUTORUN%.err
6. To configure an Autosys job in the metadata table, see the steps of Metadata Database Table Guide & Job Config Metadata Guide

### Metadata Database Table Guide
1. Metadata table can be created in any SQL Server database. The DDL script for the table creation is in `file_watcher/docs/sql/create_config_table.sql`. Only one table in the script is needed. Ignore the test table in the script.
2. Databse profile for the metadata table needs to be setup in the config file : `file_watcher/file_watch/config/db.ini`. Only the [default] profile is mandatory. You can setup optional database profiles other than default if needed.

### Job Config Metadata Guide
* job_name: required, it needs to be exactly as the Autosys job name
* app_id: required, i.e. `AGTPS`
* job_description: required or recommended, this will help troubleshooting
* file_names:  required, can be one or many file name patterns
if it's just one file, it could be a static file_name, file_name with wild card '*', or file_name with date token:format.
i.e.  `HOLDINGS.csv`
i.e.  `APX_*.csv`
i.e.  `APX_Holdings_{today:yyyy_mm_dd}.dat`
if multiple files, it has to be a comma delimted list
i.e. `APX_Holdings_{today:yyyy_mm_dd}.dat,APX_Holdings_{today:yyyy_mm_dd}.dat`
refer to date token/format documentation in `file_watcher/docs/date_token_format.md`
* file_count: required, number of files expected. the file_watcher app will only succeed if number of files satisfies this requirement
* source_path: required, could be S3 bucket with prefix `s3://my_bucket/prefix` or a network share in UNC format `\\my_share`
i.e.  `s3://allspring-us-east-1-s3-sftp-storage/wellsfargo/AGTPS/prod/inbound/`
* sleep_time: required, sleep interval in seconds. For example `30` for watching S3 bucket. Note that listing files from S3 buicket is an expensive operation, recommended sleep interval is greater than 30 seconds for S3 bucket
* look_time: required, number of times to poll the file(s). The total wait period in seconds is sleep_time multiple by look_time
* min_size: optional field, minium file size in byte(s). If left NULL, the app won't check file size. If any value greater than 0, the app will ignore any files with size less than the min_size
* exclude_age: optional field, exclude aged files in hours. If left NULL, the app won't check file age. If any value greater than 0, the app will ignore any files with age greater than exclude_age
* use_copy: optional bit (boolean) field, 1 means true, 0 means false. If it's set to be 1, it expects target_path to be setup, so that whenever file(s) are ready in the source path, the app will copy the file(s) to the target path.
* copy_names: place holder.  Leave it to NULL. This feature is not implemented. If file_copy is enabled, it will keep the same file name(s)
* target_path: required if and only if use_copy=1, this is usually the down-stream importer's app inbound folder (local folder). In rare situation, this can also be UNC network share or S3 bucket.
* use_archive: optional bit (boolean) field, 1 means true, 0 means false. If it's set to be 1, it expects archive_path to be setup, so that whenever files(s) are ready in the source path, the app will archive the file(s) to the target path
* archive_names: place holder.  Leave it to NULL. This feature is not implemented. 
* archive_path: required if and only if use_archive=1, this could be local folder, UNC network share or S3 bucket
* offset_days: temporarily offset days in additional to the date-token logic in the file_name pattern.  Usually leave it to NULL, unless you know what you're doing. It's better figure out what's the correct date-token logic. This one is the last resort
* offset_hours: temporarily offset hours in additional to the date-token logic in the file_name pattern.  Usually leave it to NULL, unless you know what you're doing. It's better figure out what's the correct date-token logic. This one is the last resort
* exclude_processed_files: optional bit (boolean) field, if it's set to 1, it turns on the logic to ignore already processed file(s) by looking up `last_processed_file_datetime` column
* file_required: optional bit (boolean) fields, if it's NULL or 1, the file is required for the app. If during the wait/polling period, file(s) doesn't arrive, the app will return a non-zero code causing Autosys job fail. If it's set to be 0, the Autosys job won't fail if file doesn't arrive during the wait period.

### Executing program

* How to run the program   
```
python -m file_watch [--debug] [--db db_profile] job_name
```
examples
```
python -m file_watch test_job
```
another example to run from Autosys command, use an environment variable for the Python virtual environment
```
%PYATHON_VENV~ -m file_watch test_job
```

## Help

Reach out to Chenggang Wang if you have any questions.
```
python -m file_watch --help
```

## Authors

Contributors names and contact info

Chenggang Wang  
cwang@allspringglobal.com

## Version History

* 0.1
    * Initial Release
* 0.1.6 stable version for TPS and Trade Rotation, with feature of excluded processed files

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

