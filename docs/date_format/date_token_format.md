## file watcher supported date token and format  

To embed date token and format in the filename, one and only one variable wrapped with curly brace. 
Syntax: {<date-token>:<date-format-string>}
For example:  RIC_APX_Holdings_{yyyyMMdd}.dat  
another example: Transactions_{today:MM-dd-yyyy}.dat  

Date-format string is .NET Date Format string which is more user-friendly

List of supported date token

Date Token | Meaning 
:------------ | :------------------ 
'today' | current system date
'today_pm' | deplayed today (today with default -20 offset_hours) 
'lastwday' | last week day relative to current system date
'lastday' | last day relative to current system date,
'lastbday'| last business day
'lbdom'  |  last business day of last month
'ldom'  | last day of last month
'fbdom' | first business day of the current month
'fdom'  | first day of the current month