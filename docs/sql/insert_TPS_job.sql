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
      min_size,
      exclude_age,
      use_copy,
      copy_names,
      target_path,
      use_archive,
      archive_names,
      archive_path,
      offset_days,
      offset_hours
  )
  VALUES
  (   'AGTPS_ric_apx_files_watch',   -- job_name - varchar(50)
      'AGTPS',   -- app_id - varchar(10)
      'Use PM_Watch to watch, deliver and archive 5 ric_apx_*_YYYYmmdd.dat files', -- job_description - varchar(200)
      'RIC_APX_Accounts_{yyyyMMdd}.dat,RIC_APX_Holdings_{yyyyMMdd}.dat,RIC_APX_Previous_Month_End_Holdings_{yyyyMMdd}.dat,RIC_APX_Securities_{yyyyMMdd}.dat,RIC_APX_Transactions_{yyyyMMdd}.dat',   -- file_names - varchar(2000)
      5,    -- file_count - int
      's3://allspring-us-east-1-s3-sftp-storage/wellsfargo/AGTPS/prod/inbound/',   -- source_path - varchar(500)
      30,    -- sleep_time - int
      300,    -- look_time - int
      NULL, -- min_size - int
      NULL, -- exclude_age - int
      1, -- use_copy - bit
      NULL, -- copy_names - varchar(2000)
      'D:\Apps\AGTPS\theWarehouse_Import\inbound', -- target_path - varchar(500)
      1, -- use_archive - bit
      NULL, -- archive_names - varchar(2000)
      's3://s3-agtps01-use-dev/AGTPS/Archive/inbound/', -- archive_path - varchar(500)
      NULL, -- offset_days - int
      NULL  -- offset_hours - int
      )