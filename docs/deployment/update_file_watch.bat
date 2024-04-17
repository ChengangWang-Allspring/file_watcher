@ECHO OFF

SET SOURCE_PATH=\\Applicationfs.awsad.allspringglobal.com\FUNFI\Build_Artifacts\file_watch_0_1_14\file_watch
SET TARGET_PATH=D:\Deployments\file_watch

ECHO SOURCE_PATH: %SOURCE_PATH%
ECHO TARGET_PATH: %TARGET_PATH%

xcopy %SOURCE_PATH% %TARGET_PATH% /S /K /Y

ECHO ALL DONE !!!

