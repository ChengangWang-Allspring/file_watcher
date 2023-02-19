-- test_901
insert file_watch_config_test (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_901','TEST_9XX','Integration Test local path watch', 'dummy_{yyyyMMdd}_*.dat', 2, 'C:\cwang\workspace-py\file_watcher\tests\integration\data\source', 1,60 )