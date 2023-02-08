USE [tpsServices]
GO

/****** Object:  Table [dbo].[pm_watch_job_config]    Script Date: 2/7/2023 9:30:25 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[pm_watch_job_config](
	[job_name] [VARCHAR](50) NOT NULL,
	[app_id] [VARCHAR](10) NOT NULL,
	[job_description] [VARCHAR](100) NULL,
	[file_name] [VARCHAR](200) NOT NULL,
	[file_count] [INT] NOT NULL,
	[source_path] [VARCHAR](200) NOT NULL,
	[sleep_time] [INT] NOT NULL,
	[look_time] [INT] NOT NULL,
	[min_size] [INT] NULL,
	[exclude_age] [INT] NULL,
	[use_copy] [BIT] NULL,
	[copy_name] [VARCHAR](200) NULL,
	[copy_path] [VARCHAR](200) NULL,
	[use_archive] [BIT] NULL,
	[archive_name] [VARCHAR](200) NULL,
	[archive_path] [VARCHAR](200) NULL,
	[offset_days] [INT] NULL,
	[offset_hours] [INT] NULL,
 CONSTRAINT [PK_pm_watch_job_config] PRIMARY KEY CLUSTERED 
(
	[job_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
