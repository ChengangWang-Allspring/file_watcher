# File Watcher CLI Application (version 0.1.11)

A file watcher application build in Python, as a supplement for the Autosys workload scheduling. 

## Description

The file watcher is for watching, validating and transferring one or multiple files from a source location (S3 bucket or network share), to application inbound folder on EC2 server. The current build is only tested in Windows Server. 

## Version History
* branch 0.1.11 (Dec 14, 2023): Fixed a bug related to "exclude_processed_files" feature. Last modified date-time on windows OS is microseconds-precision, whereas SQL Server is milli-seconds precision. Previously this caused the same file on FSX share copied again and again. 
* branch 0.1.10 (Nov 15, 2023): 
Multi date-tokens for filename(s), 
added decompress feature with new column `files_decompress` (supporting .gz and .zip)
fixed S3 to UNC copy error caused Path.resolve(). Randomly for UNC Path.resolve() adds \\?\UNC\ before \applicationfs.awsad.allspringglobal.com\{appID} causing S3 to FSX copy error. Using Path.absolute() fix the issue. 
added optional file_watch_calendar table, so that holiday can be overriden with TRUE or FALSE flag.
* branch 0.1.9  (Nov 01, 2023): Remi team requested new date-token `nextBizDay`, I also added `nextWeekDay` and `nextDay`
* branch 0.1.8  (Oct 17, 2023): GPARMS team came across an random FSX issue, had to change from .resolve() to .absolute() for line 105. It's not well documented function. Use it at your own risk. This branch is not checked in master
* version 0.1.7 (Oct 3, 2023): changed exit code to 12345 when file not found and file_required=0
* version 0.1.6 (May 19, 2023): added feature: exclude_processed_files and file_required flag for a special use case in Trade Rotation application
* version 0.1.5 (Feb 22, 2023): initial release of File watcher for AGTPS application (will be used by Fundamental Fixed Income apps such as Radar, MoneyFunds Workspace too) 

## Getting Started

 See the installation guide below.

### Dependencies

* Python 3.11
* ex. Windows 10
* `requirements.txt` for installation of 3rd party packages in the Python virtual environment


### File Watcher App - EC2 Windows Installation Guide

1. install Python 3.11 (for all users, so that it installs to `C:\Program Files\Python311`). Make sure  add-on is included.
2. Set up a virtual environment using installed version of Python 3.11: d:\Apps\common\python_venv\venv_311_pm_watch
using the following command as an example   
`python -m venv D:\Apps\common\python_venv\venv_311_pm_watch`
3. To activate the virtual environment, open a command prompt, and run   `D:\Apps\common\python_venv\venv_311_pm_watch\Scripts\activate.bat`
4. If and only if the Python virtual environment is activated (you can tell by a parenthesis `(venv_311_pm_watch)` on the left in command prompt), run the below command:  
`pip install -r D:\requirements.txt` 
, which installs 3rd parth packages in the Python virtual environment
5. Setup system environment variable:    
`PYTHON_VENV`  =  D:\Apps\common\python_venv\venv_311_pm_watch\Scripts\python.exe
6. Setup another system environment variable:   
`PYTHONPATH` = D:\Apps\common
7. Xcopy the whole python sub-folder `file_watch` from `file_watcher` (file_watcher is the root of the project) to   
`D:\Apps\common`
8. Use the following command in the Autosys File_Watch job   
command = ```%PYTHON_VENV% -m file_watch %AUTO_JOB_NAME%```   
Standard output file = `>D:\Apps\Logs\%AUTO_JOB_NAME%_%AUTORUN%.out`   
Standard error file = `>D:\Apps\Logs\%AUTO_JOB_NAME%_%AUTORUN%.err`
9. To configure an Autosys job in the metadata table, see the steps of `Metadata Database Table Guide` & `Job Config Metadata Guide`

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
* file_required: optional bit (boolean) fields, if it's NULL or 1, the file is required for the app. If during the wait/polling period, file(s) doesn't arrive, the app will return a non-zero code causing Autosys job fail. If it's set to be 0, the Autosys job won't fail if file doesn't arrive during the wait period (it will silently return `12345` without throwing error).
* files_decompress: optional comma seperated list of file-extension that need to be decompressed, i.e `.zip,.gz` (introduced in version 0.1.10)
* calendar_name: optional holiday calendar by key 'calendar_name' to tell if it's a TRUE holiday or FALSE holiday. By default file_watch use federal US Holidays calulated from Python module. To check what are the default US holidays by file_watch program, you can run the command `python -m file_watch.util.holiday 2023`, for which 2023 is the year parameter. (introduced in version 0.1.10)

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


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

