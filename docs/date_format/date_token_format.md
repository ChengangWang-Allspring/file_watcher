## file watcher supported date token and format  

Date-format string is .NET Date Format string which is more user-friendly

To embed date token and format in the filename, one and only one variable wrapped with curly brace. All the date tokens are relative to the current system date where the Python program runs.

Syntax: {date-token:date-format-string}
For example:  RIC_APX_Holdings_{yyyyMMdd}.dat  
another example: Transactions_{today:MM-dd-yyyy}.dat  

default date-token is {today}.  
default date-format-string is {yyyyMMdd}. 
basically {yyyyMMdd} is equivalent to {today}, and it's also equivalent to {today:yyyyMMdd} 

List of supported date token 

Date Token | Meaning 
:------------ | :------------------ 
'today' | current date
'today_Pm' | yesterday before 8pm, today after 8pm
'prevWeekDay' | previous week day 
'prevDay' | previous day  
'prevBizDay'| previous business day
'lastBizDayOfLastMnth'  |  last business day of last month
'lastDayOfLastMnth'  | last day of last month
'firsBizDayOfMnth' | first business day of the current month
'firsDayOfMnth'  | first day of the current month