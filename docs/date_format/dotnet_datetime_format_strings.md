## Cheat sheet with C# DateTime formats.

Date and Time in C# are handled by DateTime class in C# that provides properties and methods to format dates in different datetime formats. This article blog explains how to work with date and time format in C#. 

The following table describes various C# DateTime formats and their results. Here we see all the patterns of the C# DateTime, format, and results.

### Examples
Format | Result
:----- | :--------------------------
DateTime.Now.ToString("MM/dd/yyyy") | 05/29/2015
DateTime.Now.ToString("dddd, dd MMMM yyyy") | Friday, 29 May 2015
DateTime.Now.ToString("dddd, dd MMMM yyyy") | Friday, 29 May 2015 05:50
DateTime.Now.ToString("dddd, dd MMMM yyyy") | Friday, 29 May 2015 05:50 AM
DateTime.Now.ToString("dddd, dd MMMM yyyy") | Friday, 29 May 2015 5:50
DateTime.Now.ToString("dddd, dd MMMM yyyy") | Friday, 29 May 2015 5:50 AM
DateTime.Now.ToString("dddd, dd MMMM yyyy HH:mm:ss") | Friday, 29 May 2015 05:50:06
DateTime.Now.ToString("MM/dd/yyyy HH:mm") | 05/29/2015 05:50
DateTime.Now.ToString("MM/dd/yyyy hh:mm tt") | 05/29/2015 05:50 AM
DateTime.Now.ToString("MM/dd/yyyy H:mm") | 05/29/2015 5:50
DateTime.Now.ToString("MM/dd/yyyy h:mm tt") | 05/29/2015 5:50 AM
DateTime.Now.ToString("MM/dd/yyyy HH:mm:ss") | 05/29/2015 05:50:06
DateTime.Now.ToString("MMMM dd") | May 29
DateTime.Now.ToString("yyyy’-‘MM’-‘dd’T’HH’:’mm’:’ss.fffffffK") | 2015-05-16T05:50:06.7199222-04:00
DateTime.Now.ToString("ddd, dd MMM yyy HH’:’mm’:’ss ‘GMT’") | Fri, 16 May 2015 05:50:06 GMT
DateTime.Now.ToString("yyyy’-‘MM’-‘dd’T’HH’:’mm’:’ss") | 2015-05-16T05:50:06
DateTime.Now.ToString("HH:mm") | 05:50
DateTime.Now.ToString("hh:mm tt") | 05:50 AM
DateTime.Now.ToString("H:mm") | 5:50
DateTime.Now.ToString("h:mm tt") | 5:50 AM
DateTime.Now.ToString("HH:mm:ss") | 05:50:06
DateTime.Now.ToString("yyyy MMMM") | 2015 May


### List of DateTime format string
- d -> Represents the day of the month as a number from 1 through 31.
- dd -> Represents the day of the month as a number from 01 through 31.
- ddd-> Represents the abbreviated name of the day (Mon, Tues, Wed, etc).
- dddd-> Represents the full name of the day (Monday, Tuesday, etc).
- h-> 12-hour clock hour (e.g. 4).
- hh-> 12-hour clock, with a leading 0 (e.g. 06)
- H-> 24-hour clock hour (e.g. 15)
- HH-> 24-hour clock hour, with a leading 0 (e.g. 22)
- m-> Minutes
- mm-> Minutes with a leading zero
- M-> Month number(eg.3)
- MM-> Month number with leading zero(eg.04)
- MMM-> Abbreviated Month Name (e.g. Dec)
- MMMM-> Full month name (e.g. December)
- s-> Seconds
- ss-> Seconds with leading zero
- t-> Abbreviated AM / PM (e.g. A or P)
- tt-> AM / PM (e.g. AM or PM
- y-> Year, no leading zero (e.g. 2015 would be 15)
- yy-> Year, leading zero (e.g. 2015 would be 015)
- yyy-> Year, (e.g. 2015)
- yyyy-> Year, (e.g. 2015)
- K-> Represents the time zone information of a date and time value (e.g. +05:00)
- z-> With DateTime values represents the signed offset of the local operating system's time zone from
- Coordinated Universal Time (UTC), measured in hours. (e.g. +6)
- zz-> As z, but with leading zero (e.g. +06)
- zzz-> With DateTime values represents the signed offset of the local operating system's time zone from UTC, measured in hours and minutes. (e.g. +06:00)
- f-> Represents the most significant digit of the seconds' fraction; that is, it represents the tenths of a second in a date and time value.
- ff-> Represents the two most significant digits of the seconds' fraction in date and time
- fff-> Represents the three most significant digits of the seconds' fraction; that is, it represents the milliseconds in a date and time value.
- ffff-> Represents the four most significant digits of the seconds' fraction; that is, it represents the ten-thousandths of a second in a date and time value. While it is possible to display the ten-thousandths of a second component of a time value, that value may not be meaningful.
- fffff-> Represents the five most significant digits of the seconds' fraction; that is, it represents the hundred-thousandths of a second in a date and time value.
- ffffff-> Represents the six most significant digits of the seconds' fraction; that is, it represents the millionths of a second in a date and time value.
- fffffff-> Represents the seven most significant digits of the second's fraction; that is, it represents the ten-millionths of a second in a date and time value.
 
