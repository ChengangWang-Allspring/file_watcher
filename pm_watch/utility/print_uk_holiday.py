from datetime import date
import holidays

# Select country
uk_holidays = holidays.UnitedKingdom()

# Print all the holidays in UnitedKingdom in year 2018
for ptr in holidays.UnitedKingdom(years=2023).items():
    print(ptr)
