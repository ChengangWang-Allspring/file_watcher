use tpsServices
GO

DELETE FROM pm_watch_job_config WHERE app_id='TEST'

-- test_1: Test local path, single file
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_1','TEST','Test local path, single file', 'RIC_APX_Holdings_{yyyyMMdd}.dat', 1, 'C:\cwang\Apps\inbound', 5,20 )

-- test_2: Test UNC path, single file
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_2','TEST',' Test UNC path, single file', 'RIC_APX_Holdings_{yyyyMMdd}.dat', 1, '\\10.24.38.59\Deployments\test_inbound', 5,20 )

-- test_3: Test S3 path, single file  
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_3','TEST','Test S3 path, single file ', 'RIC_APX_Holdings_{yyyyMMdd}.dat', 1, 's3://s3-agtps01-use-dev/AGTPS/inbound/', 10,20 )


-- test_4: Test S3 path, multiple file  
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_4','TEST','Test S3 path, multiple file  ', 'RIC_APX_*_{yyyyMMdd}.dat', 5, 's3://s3-agtps01-use-dev/AGTPS/inbound/', 10,20 )


-- test_5: Test S3 path, multiple file, more restrictive filenames  
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_5','TEST','Test S3 path, multiple file, more restrictive filenames', 'RIC_APX_Accounts_{yyyyMMdd}.dat,RIC_APX_Holdings_{yyyyMMdd}.dat,RIC_APX_Previous_Month_End_Holdings_{yyyyMMdd}.dat,RIC_APX_Securities_{yyyyMMdd}.dat,RIC_APX_Transactions_{yyyyMMdd}.dat', 5, 's3://allspring-us-east-1-s3-sftp-storage/wellsfargo/AGTPS/prod/inbound/', 10,20 )

-- test_6: Test error: bad source_path
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_6','TEST','Test error: bad source_path ', 'RIC_APX_Accounts_{yyyyMMdd}.dat', 1, 'BAD_PATH:\BAD_PATH', 10,20 )

-- test_7: Test error: bad file_names variable
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_7','TEST','Test error: bad bad file_names variable', 'RIC_APX_Accounts_{#$@#$@:yyyyMMdd}.dat', 1, 'C:\cwang\Apps\inbound', 5,10 )

-- test_8: Test error: missing file_names
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_8','TEST','Test error: missing app_id, file_names', '', 0, 'C:\cwang\Apps\inbound', 5,10 )

-- test_9: Test date tokens & formats
insert pm_watch_job_config (job_name, app_id, job_description, file_names, file_count, source_path, sleep_time,look_time)
values ('test_9','TEST','Test date tokens & formats', 'a_{yyyyMMdd}.txt,b_{today}.txt,c_{today:yyyyMMdd}.txt,d_{today_pm:yyMMdd}.txt,e_{lastwday:yyyy_MM_dd}.txt,f_{lastday:MM-dd-yyyy}.txt,g_{lastbday:yyyyMMdd}.txt,h_{lbdom:MM-dd-yyyy}.txt,i_{ldom:MM_dd_yyyy}.txt', 100, 'C:\cwang\Apps\inbound', 5,10 )

SELECT * FROM pm_watch_job_config WHERE app_id='TEST'

