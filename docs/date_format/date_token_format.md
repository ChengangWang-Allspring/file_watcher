## file watcher supported date token and format  

Date-format string is .NET Date Format string which is more user-friendly

To embed date token and format in the filename, one or multiple variable(s) wrapped with curly brace. All the date tokens are relative to the current system date where the Python program runs.

Syntax: {date-token:date-format-string}
For example:  RIC_APX_Holdings_{yyyyMMdd}.dat  
another example: Transactions_{today:MM-dd-yyyy}.dat 
multi-tokens example:  prefix_{today:yyyy}_middle_{today:MM-dd}.csv 

default date-token is {today}.  
default date-format-string is {yyyyMMdd}. 
basically {yyyyMMdd} is equivalent to {today}, and it's also equivalent to {today:yyyyMMdd} 

List of supported date token 

Date Token | Meaning 
:------------ | :------------------ 
'today' | current date
'todayPm' | yesterday before 8pm, today after 8pm
'prevWeekDay' | previous week day 
'prevWeekDayPm' | previous weekday using todayPm logic
'prevDay' | previous day  
'prevBizDay'| previous business day
'lastBizDayOfPrevMnth'  |  last business day of last month
'lastDayOfPrevMnth'  | last day of last month
'firsBizDayOfMnth' | first business day of the current month
'firsDayOfMnth'  | first day of the current month
'nextWeekDay' | next week day 
'nextWeekDayPm' | next weekday using todayPm logic
'nextDay' | next day  
'nextBizDay'| next business day
