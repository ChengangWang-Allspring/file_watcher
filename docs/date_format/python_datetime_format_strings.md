## Python 3.11 strftime() format string 

The strftime() function is used to convert date and time objects to their string representation. It takes one or more input of formatted code and returns the string representation.

Syntax :

strftime(format)
Returns : It returns the string representation of the date or time object.

List of format codes : Reference table for the format codes.

Directive | Meaning | Output Format
:-------- | :------ | :-------------- 
%a | Abbreviated weekday name. | Sun, Mon, …
%A | Full weekday name. | Sunday, Monday, …
%w | Weekday as a decimal number. | 0, 1, …, 6
%d | Day of the month as a zero added decimal. | 01, 02, …, 31
%#d | Day of the month as a decimal number. | 1, 2, …, 30
%b | Abbreviated month name. | Jan, Feb, …, Dec
%B | Full month name. | January, February, …
%m | Month as a zero added decimal number. | 01, 02, …, 12
%#m | Month as a decimal number. | 1, 2, …, 12
%y | Year without century as a zero added decimal number. | 00, 01, …, 99
%#y | Year without century as a decimal number. | 0, 1, …, 99
%Y | Year with century as a decimal number. | 2013, 2019 etc.
%H | Hour (24-hour clock) as a zero added decimal number. | 00, 01, …, 23
%#H | Hour (24-hour clock) as a decimal number. | 0, 1, …, 23
%I | Hour (12-hour clock) as a zero added decimal number. | 01, 02, …, 12
%#I | Hour (12-hour clock) as a decimal number. | 1, 2, … 12
%p | Locale’s AM or PM. | AM, PM
%M | Minute as a zero added decimal number. | 00, 01, …, 59
%#M | Minute as a decimal number. | 0, 1, …, 59
%S | Second as a zero added decimal number. | 00, 01, …, 59
%#S | Second as a decimal number. | 0, 1, …, 59
%f | Microsecond as a decimal number, zero added on the left. | 000000 – 999999
%z | UTC offset in the form +HHMM or -HHMM. |  
%Z | Time zone name. |  
%j | Day of the year as a zero added decimal number. | 001, 002, …, 366
%#j | Day of the year as a decimal number. | 1, 2, …, 366
%U | Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, …, 53
%W | Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0. | 00, 01, …, 53