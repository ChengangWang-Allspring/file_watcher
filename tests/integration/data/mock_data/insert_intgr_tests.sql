SELECT * FROM dbo.file_watch_config_test WHERE job_name LIKE 'INTGR_TEST_%'

DELETE FROM   dbo.file_watch_config_test WHERE job_name LIKE 'INTGR_TEST_%'

-- INTGR_TEST_1
insert file_watch_config_test (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('INTGR_TEST_1','INTGR_TEST','Local path watch', 'dummy_{yyyyMMdd}_*.dat', 2, 'c:\temp\tests\integration\source', 1,60 )

-- INTGR_TEST_2
insert file_watch_config_test (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, use_copy, target_path)
values ('INTGR_TEST_2','INTGR_TEST','Local path watch, copy', 'dummy_{today}_*.dat', 5, 'c:\temp\tests\integration\source', 1,60, 1, 'c:\temp\tests\integration\inbound')

-- INTGR_TEST_3
insert file_watch_config_test (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, use_copy, target_path, use_archive, archive_path)
values ('INTGR_TEST_3','INTGR_TEST','Local path watch, copy, archive', 'dummy_{todayPm:yyyy-MM-dd}_*.dat', 3, 'c:\temp\tests\integration\source', 1,60, 1, 'c:\temp\tests\integration\inbound',1,'c:\temp\tests\integration\archive')

-- INTGR_TEST_4
insert file_watch_config_test (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('INTGR_TEST_4','INTGR_TEST','s3 watch', 'dummy_{todayPm:yyyy-MM-dd}_*.dat', 3, 's3://s3-agtps01-use-dev/tests/integration/source/', 2,30 )
