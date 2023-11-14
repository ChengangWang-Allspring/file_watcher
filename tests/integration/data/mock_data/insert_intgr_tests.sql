SELECT *
FROM dbo.file_watch_config_test
WHERE job_name LIKE 'INTGR_TEST_%'

DELETE FROM   dbo.file_watch_config_test WHERE job_name LIKE 'INTGR_TEST_%'

-- INTGR_TEST_1
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values
  ('INTGR_TEST_1', 'INTGR_TEST', 'Local path watch', 'daily_{yyyyMMdd}_accounts.dat,daily_{yyyyMMdd}_security.dat', 2, 'c:\temp\tests\integration\source', 1, 10 )

-- INTGR_TEST_2
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, use_copy, target_path)
values
  ('INTGR_TEST_2', 'INTGR_TEST', 'FSX to Local path watch, copy', 'dummy_{today}_*.dat', 5, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\Inbound', 1, 10, 1, 'c:\temp\tests\integration\inbound')

-- INTGR_TEST_3
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, use_copy, target_path, use_archive, archive_path)
values
  ('INTGR_TEST_3', 'INTGR_TEST', 'FSX to FSX path watch, copy, archive', 'dummy_{todayPm:yyyy-MM-dd}_*.dat', 1, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\MFT\Inbound', 1, 10, 1, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\Inbound', 1, 'c:\temp\tests\integration\archive')

-- INTGR_TEST_4
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values
  ('INTGR_TEST_4', 'INTGR_TEST', 's3 watch', 'A_{prevWeekDay:yyyy_MM_dd}.dat, B_{prevWeekDay:yyyy_MM_dd}.dat', 2, 's3://s3-agtps01-use-dev/tests/integration/source/', 1, 10 )

-- INTGR_TEST_5
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time,use_copy, target_path, use_archive, archive_path)
values
  ('INTGR_TEST_5', 'INTGR_TEST', 's3 watch, copy local, archive FSX', 'sample_{prevBizDay:MM_dd_yyyy}_*.dat', 5, 's3://s3-agtps01-use-dev/tests/integration/source/', 1, 10, 1, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\Inbound', 1, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\Archive\Inbound' )


-- INTGR_TEST_6
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time,use_copy, target_path, use_archive, archive_path)
values
  ('INTGR_TEST_6', 'INTGR_TEST', 's3 watch, copy s3, archive local', 'report_{prevBizDay:MM_dd_yyyy}_*.dat', 5, 's3://s3-agtps01-use-dev/tests/integration/source/', 1, 10, 1, '\\Applicationfs.awsad.allspringglobal.com\FUNFI\Temp\Inbound', 1, 'c:\temp\tests\integration\archive' )


-- INTGR_TEST_7
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, min_size)
values
  ('INTGR_TEST_7', 'INTGR_TEST', 's3 watch with min_size', 'A_{prevWeekDay:yyyy_MM_dd}.dat, B_{prevWeekDay:yyyy_MM_dd}.dat', 2, 's3://s3-agtps01-use-dev/tests/integration/source/', 1, 6, 1000 )


-- INTGR_TEST_8
insert file_watch_config_test
  (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time, exclude_age)
values
  ('INTGR_TEST_8', 'INTGR_TEST', 'Local path watch, exclude_age 12 hours older', 'daily_{yyyyMMdd}_accounts.dat,daily_{yyyyMMdd}_security.dat', 2, 'c:\temp\tests\integration\source', 1, 10, 12 )