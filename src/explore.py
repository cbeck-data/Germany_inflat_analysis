import numpy as np
import pandas as pd
import seaborn as sns

#--- We want to create EDA for the series we fetched

path = "./data/fred.csv"
series = pd.read_csv(path)

print(series.columns)

# the cols need renaming!


series = series.rename(columns = {'0': "Germany_CPI",
                                  'Unnamed: 0': 'Month'})

# learnings I made: 
# need to reassign the newly created series
# need tp indicate that I mean the columns, not something else
# need to provide a dictionary to transform the colnames
print("\nrenamed cols:")
print(series.columns)
print(series['Month'].dtype)
# dtype is simply object. I need to convert this to a date time year datatype. I think pandas has it

# converting to a date time object and checking the double index structure
series['Month'] = pd.to_datetime(series['Month'])

print("\nupdated structure:")
print(series['Month'].dtype)
print(series['Month'].dt.year)
print(series['Month'].dt.month)

# successful, ready for a simple line plot
series_id = series.set_index(series['Month'].dt.month)

# this keeps the "Month" col as a DateTime object, but adds an Index called "Month". Need to separate that one!
series_id = series_id.rename(columns = {'Month': 'Time_Stamp'})

print(series_id)

# this works!

# -------- there's a simpler method:

series = series.set_index('Month')

print(series) # yuppers, this works really well!

#------- Plotting

from matplotlib import pyplot as plt

plt.figure(figsize = (12, 8))
plt.plot(series.index,
         series['Germany_CPI'],
         label = "Germany CPI over time, base year = 2015",
         linewidth = 2
         )
# plt.show() # toggle this on and off for reference

series['Infl_rate'] = series['Germany_CPI'].pct_change()
print(series.head())

plt.figure(figsize = (12, 8))
plt.plot(series.index,
         series['Infl_rate'],
         label = "Germany Inflation Rate over time, base year = 2015",
         linewidth = 2
         )
plt.show()