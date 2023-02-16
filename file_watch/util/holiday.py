""" 
Holiday to display holidays
usage (to display holiday in 2023): 
    python -m file_watch.utility.holiday 2023
"""

from datetime import date
import holidays
import argparse

parser = argparse.ArgumentParser(description='print public USA holiday by year')
parser.add_argument('year', help='year in yyyy format ')
args = parser.parse_args()

year: int = 0
is_int = False
try:
    year = int(args.year)
    is_int = True
except ValueError:
    is_int = False

if is_int:
    # us_holidays = holidays.UnitedStates()  # Select country USA
    for key, value in holidays.UnitedStates(years=year).items():
        print(f'{key} :    {value}')
else:
    print('Not an integer. <year> must be in yyyy format')
