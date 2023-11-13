USE [FIIT_MetadataDB]
GO

/****** Object:  Table [dbo].[file_watch_config]    Script Date: 2/7/2023 9:30:25 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[file_watch_config]
(
	[job_name] [VARCHAR](50) NOT NULL,
	[app_id] [VARCHAR](10) NOT NULL,
	[job_description] [VARCHAR](200) NULL,
	[file_names] [VARCHAR](max) NOT NULL,
	[file_count] [INT] NOT NULL,
	[source_path] [VARCHAR](500) NOT NULL,
	[sleep_time] [INT] NOT NULL,
	[look_time] [INT] NOT NULL,
	[min_size] [INT] NULL,
	[exclude_age] [INT] NULL,
	[use_copy] [BIT] NULL,
	[copy_names] [VARCHAR](500) NULL,
	[target_path] [VARCHAR](500) NULL,
	[use_archive] [BIT] NULL,
	[archive_names] [VARCHAR](500) NULL,
	[archive_path] [VARCHAR](500) NULL,
	[offset_days] [INT] NULL,
	[offset_hours] [INT] NULL,
	[exclude_processed_files] [BIT] NULL,
	[last_processed_file_datetime] [DateTime] NULL,
	[file_required] [BIT] NULL,
	[files_decompress] [varchar] (20) NULL,
	[calendar_name] [VARCHAR](50) NULL,
	CONSTRAINT [PK_file_watch_config] PRIMARY KEY CLUSTERED 
(
	[job_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


USE [FIIT_MetadataDB]
GO

/****** Object:  Table [dbo].[file_watch_calendar]    Script Date: 11/13/2023 8:56:41 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[file_watch_calendar]') AND type IN (N'U'))
BEGIN
CREATE TABLE [dbo].[file_watch_calendar](
	[calendar_name] [VARCHAR](50) NOT NULL,
	[date] SMALLDATETIME NOT NULL,
	[is_holiday] [BIT] NOT NULL,
	[holiday_name] [VARCHAR](200) NULL,
 CONSTRAINT [PK_file_watch_holiday_override] PRIMARY KEY CLUSTERED 
(
	[calendar_name] ASC,
	[date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO





USE [tpsServices]
GO

/****** Object:  Table [dbo].[file_watch_config_test]    Script Date: 2/15/2023 8:36:07 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[file_watch_config_test]
(
	[job_name] [VARCHAR](50) NOT NULL,
	[app_id] [VARCHAR](10) NOT NULL,
	[job_description] [VARCHAR](200) NULL,
	[file_names] [VARCHAR](max) NOT NULL,
	[file_count] [INT] NOT NULL,
	[source_path] [VARCHAR](2000) NOT NULL,
	[sleep_time] [INT] NOT NULL,
	[look_time] [INT] NOT NULL,
	[min_size] [INT] NULL,
	[exclude_age] [INT] NULL,
	[use_copy] [BIT] NULL,
	[copy_names] [VARCHAR](2000) NULL,
	[target_path] [VARCHAR](2000) NULL,
	[use_archive] [BIT] NULL,
	[archive_names] [VARCHAR](2000) NULL,
	[archive_path] [VARCHAR](2000) NULL,
	[offset_days] [INT] NULL,
	[offset_hours] [INT] NULL,
	[exclude_processed_files] [BIT] NULL,
	[last_processed_file_datetime] [DateTime] NULL,
	[file_required] [BIT] NULL,
	[files_decompress] [varchar] (20) NULL,
	CONSTRAINT [PK_file_watch_config_test] PRIMARY KEY CLUSTERED 
(
	[job_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
