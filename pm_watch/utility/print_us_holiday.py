from datetime import date
import holidays

# Select country
us_holidays = holidays.UnitedStates()

# Print all the holidays in UnitedKingdom in year 2018
for ptr in holidays.UnitedStates(years=2023).items():
    print(ptr)
