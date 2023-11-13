USE FIIT_MetadataDB
GO

INSERT dbo.file_watch_config
(
    job_name,
    app_id,
    job_description,
    file_names,
    file_count,
    source_path,
    sleep_time,
    look_time,
	use_copy,
	target_path,
    files_decompress

)
VALUES
(   'Test_100',      -- job_name - varchar(50)
    'TEST',      -- app_id - varchar(10)
    'Test decompress and holiday override',    -- job_description - varchar(200)
    'RIC_APX_{yyyyMMdd}.zip,test_{yyyy-MM-dd}.out.gz',      -- file_names - varchar(max)
    2,       -- file_count - int
    'C:\cwang\Apps\source_location',      -- source_path - varchar(500)
    30,       -- sleep_time - int
    10,       -- look_time - int
    1,
	'C:\cwang\Apps\inbound',
	'.zip,.gz'
    )
