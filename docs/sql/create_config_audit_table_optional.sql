PRINT 'SCRIPT FILE NAME: DEPLOY_AGTRR_AUTOSYS_FILEWATER_AUDIT_TBL_DDL.sql'
GO
PRINT 'SERVER NAME: ' + @@SERVERNAME
GO
PRINT '--######################'
GO

--#########
--#########
--#########
--#########
USE FIIT_MetadataDB
GO
PRINT '#####DB: '+DB_NAME()	
GO
PRINT '@@@@@@@@@START --alter file_watch_config add last update and create user cols'
GO

IF NOT EXISTS (SELECT 1 FROM sys.objects o
          INNER JOIN sys.columns c ON o.object_id = c.object_id
          WHERE o.name = 'file_watch_config' AND c.name = 'last_upd_date')
	ALTER TABLE [dbo].[file_watch_config] ADD [last_upd_date] [DATETIME] NOT NULL DEFAULT GETDATE()
GO

IF NOT EXISTS (SELECT 1 FROM sys.objects o
          INNER JOIN sys.columns c ON o.object_id = c.object_id
          WHERE o.name = 'file_watch_config' AND c.name = 'last_upd_user')
	ALTER TABLE [dbo].[file_watch_config] ADD [last_upd_user] [NVARCHAR](100) NOT NULL DEFAULT USER_NAME()
GO	

IF NOT EXISTS (SELECT 1 FROM sys.objects o
          INNER JOIN sys.columns c ON o.object_id = c.object_id
          WHERE o.name = 'file_watch_config' AND c.name = 'create_date')
	ALTER TABLE [dbo].[file_watch_config] ADD [create_date] [DATETIME] NOT NULL DEFAULT GETDATE()
GO	

IF NOT EXISTS (SELECT 1 FROM sys.objects o
          INNER JOIN sys.columns c ON o.object_id = c.object_id
          WHERE o.name = 'file_watch_config' AND c.name = 'create_user')
	ALTER TABLE [dbo].[file_watch_config] ADD [create_user] [NVARCHAR](100) NOT NULL DEFAULT USER_NAME()
GO
PRINT '@@@@@@@@@Done --alter file_watch_config add last update and create user cols'

PRINT '@@@@@@@@@START --create [file_watch_config_audit] table'
GO

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[file_watch_config_audit]') AND type IN (N'U'))
DROP TABLE [dbo].[file_watch_config_audit]
GO

CREATE TABLE [dbo].[file_watch_config_audit](	
    [id] [BIGINT] IDENTITY(1,1) NOT NULL,
	[job_name] [varchar](100) NOT NULL,
	[app_id] [varchar](10) NOT NULL,
	[job_description] [varchar](200) NULL,
	[file_names] [varchar](max) NOT NULL,
	[file_count] [int] NOT NULL,
	[source_path] [varchar](500) NOT NULL,
	[sleep_time] [int] NOT NULL,
	[look_time] [int] NOT NULL,
	[min_size] [int] NULL,
	[exclude_age] [int] NULL,
	[use_copy] [bit] NULL,
	[copy_names] [varchar](500) NULL,
	[target_path] [varchar](500) NULL,
	[use_archive] [bit] NULL,
	[archive_names] [varchar](500) NULL,
	[archive_path] [varchar](500) NULL,
	[offset_days] [int] NULL,
	[offset_hours] [int] NULL,
	[exclude_processed_files] [bit] NULL,
	[last_processed_file_datetime] [datetime] NULL,
	[file_required] [bit] NULL,
	[files_decompress] [varchar] (20) NULL,
	[calendar_name] varchar(50) NULL,
	[last_upd_date] [DATETIME] NOT NULL,
	[last_upd_user] [NVARCHAR](100) NOT NULL,
	[create_date] [DATETIME] NOT NULL,
	[create_user] [NVARCHAR](100) NOT NULL,
	[updated_at] [DATETIME] NOT NULL,
	[operation] [CHAR](3) NOT NULL  
)


PRINT '@@@@@@@@@DONE --create [file_watch_config_audit] table'
GO




PRINT '@@@@@@@@@START --create user file_watch_config CRUD triggers'
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[TR_file_watch_config_AfterDelete]
ON dbo.file_watch_config
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
	    
	IF NOT EXISTS(SELECT * FROM INSERTED)
		BEGIN
			IF NOT EXISTS(SELECT * FROM DELETED) RETURN;
			ELSE			
				INSERT INTO dbo.file_watch_config_audit
				(	job_name,
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
					offset_hours,
					exclude_processed_files,
					last_processed_file_datetime,
					file_required,
					files_decompress,
					calendar_name,
					last_upd_date,
					last_upd_user,
					create_date,
					create_user,
					updated_at,
					operation
				)
				SELECT
					A.job_name,
					A.app_id,
					A.job_description,
					A.file_names,
					A.file_count,
					A.source_path,
					A.sleep_time,
					A.look_time,
					A.min_size,
					A.exclude_age,
					A.use_copy,
					A.copy_names,
					A.target_path,
					A.use_archive,
					A.archive_names,
					A.archive_path,
					A.offset_days,
					A.offset_hours,
					A.exclude_processed_files,
					A.last_processed_file_datetime,
					A.file_required,
					A.files_decompress,
					A.calendar_name,
					A.last_upd_date,
					A.last_upd_user,
					A.create_date,
					A.create_user,
					GETDATE(),
					'DEL'
				FROM
					DELETED A
		END
    ELSE 
        RETURN;
END;
GO

ALTER TABLE dbo.file_watch_config ENABLE TRIGGER [TR_file_watch_config_AfterDelete]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[TR_file_watch_config_AfterInsert]
ON dbo.file_watch_config
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
	    
	IF EXISTS(SELECT * FROM INSERTED)
		BEGIN
			IF EXISTS(SELECT * FROM DELETED) RETURN;
			ELSE
				INSERT INTO dbo.file_watch_config_audit
				(	job_name,
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
					offset_hours,
					exclude_processed_files,
					last_processed_file_datetime,
					file_required,
					files_decompress,
					calendar_name,
					last_upd_date,
					last_upd_user,
					create_date,
					create_user,
					updated_at,
					operation
				)
				SELECT
					A.job_name,
					A.app_id,
					A.job_description,
					A.file_names,
					A.file_count,
					A.source_path,
					A.sleep_time,
					A.look_time,
					A.min_size,
					A.exclude_age,
					A.use_copy,
					A.copy_names,
					A.target_path,
					A.use_archive,
					A.archive_names,
					A.archive_path,
					A.offset_days,
					A.offset_hours,
					A.exclude_processed_files,
					A.last_processed_file_datetime,
					A.file_required,
					A.files_decompress,
					A.calendar_name,
					A.last_upd_date,
					A.last_upd_user,
					A.create_date,
					A.create_user,
					GETDATE(),
					'INS'
				FROM
					INSERTED A
		END
    ELSE 
        RETURN;
END;
GO

ALTER TABLE dbo.file_watch_config ENABLE TRIGGER [TR_file_watch_config_AfterInsert]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER TRIGGER [dbo].[TR_file_watch_config_AfterUpdate]
ON dbo.file_watch_config
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
	    
	IF EXISTS(SELECT * FROM INSERTED)
		BEGIN
			IF NOT EXISTS(SELECT * FROM DELETED) RETURN;
			ELSE
				INSERT INTO dbo.file_watch_config_audit
				(	job_name,
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
					offset_hours,
					exclude_processed_files,
					last_processed_file_datetime,
					file_required,
					files_decompress,
					calendar_name,
					last_upd_date,
					last_upd_user,
					create_date,
					create_user,
					updated_at,
					operation
				)
				SELECT
					A.job_name,
					A.app_id,
					A.job_description,
					A.file_names,
					A.file_count,
					A.source_path,
					A.sleep_time,
					A.look_time,
					A.min_size,
					A.exclude_age,
					A.use_copy,
					A.copy_names,
					A.target_path,
					A.use_archive,
					A.archive_names,
					A.archive_path,
					A.offset_days,
					A.offset_hours,
					A.exclude_processed_files,
					A.last_processed_file_datetime,
					A.file_required,
					A.files_decompress,
					A.calendar_name,
					A.last_upd_date,
					A.last_upd_user,
					A.create_date,
					A.create_user,
					GETDATE(),
					'UPD'
				FROM
					INSERTED A
				INNER JOIN DELETED D
					ON A.job_name = D.job_name
		END
    ELSE 
        RETURN;
END;
GO

ALTER TABLE dbo.file_watch_config ENABLE TRIGGER [TR_file_watch_config_AfterUpdate]
GO

PRINT '@@@@@@@@@DONE --create file_watch_config  CRUD triggers'

/*
SCRIPT FILE NAME: DEPLOY_AGTRR_AUTOSYS_FILEWATER_AUDIT_TBL_DDL.sql
SERVER NAME: EC2AMAZ-9Q9A89E
--######################
#####DB: AGTRR_Config
@@@@@@@@@START --alter file_watch_config add last update and create user cols
@@@@@@@@@Done --alter file_watch_config add last update and create user cols
@@@@@@@@@START --create [file_watch_config_audit] table
@@@@@@@@@DONE --create [file_watch_config_audit] table
@@@@@@@@@START --create user file_watch_config CRUD triggers
@@@@@@@@@DONE --create file_watch_config  CRUD triggers

Completion time: 2023-10-17T20:44:01.6934802-05:00
*/

