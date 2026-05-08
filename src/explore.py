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
# plt.show()

# this shows a potentially stationary time series now.
# What we wanna test from here is whether rho superceeds 1/-1
# visually, It doesn't seem to, but we'll do the Augmented Dickens Fuller Test

# """
# I don't know whether pandas has an ACF device,
# But it sounds pretty fun, so I'm coding one myself hehe
# """

# ACF means plotting rho on all x[t] for period k ( = 1 )

# Lets calculate rho for my differenced series:

k = [i for i in range(13)] # ugh, guess I'll use list comprehensions then
# this calculates over all 12 months
k = k[1:]
print(k) # k from 1 - 10

y = series['Infl_rate'].dropna().values # give me all non nan values for infl rate
k_record = {}
k_record[0] = 1.0
for k in k:
    y_t = y[k:] # series of all y except the first
    y_tk = y[:-k] # series of all y except the last
# this just generates, and overwrites.
# I need something that generates new vars and saves them :/
    cor_matrix = np.corrcoef(y_t, y_tk)
    cor = cor_matrix[0, 1] # line one, col two
    print(f"correlation at k = {k}: {cor}")
    print(f"len of {k}-list: {len(y_t)}")
    k_record[k] = cor
# this essentially give me a k: cor dict for plotting


plt.figure(figsize= (12, 8))
plt.stem(k_record.keys(),
         k_record.values()
         )
# plt.show()

from statsmodels.tsa.stattools import acf
acf_res = acf(x =
                                       series['Infl_rate'].dropna(),
                                       nlags = 12,
                                       alpha = 0.05,
                                       adjusted= True
                                       )
print(acf_res[0])
lag_list = range(13)
plt.figure(figsize= (12, 8))
plt.stem(lag_list,
         acf_res[0]
         )
plt.show()