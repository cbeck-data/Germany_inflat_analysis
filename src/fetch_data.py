import os
import dotenv
import fredapi

# setting up my directory, environment, and fetching the key from environment
# print(os.getcwd()) 

dotenv.load_dotenv()
os.environ

# print(os.environ.items()) # testing whether this is a dictionary


key = os.environ.get("FRED_API_KEY") # fetching key

client = fredapi.Fred(key) # creating fred client object based on fred api key

example = client.get_series("DEUCPIALLMINMEI") # testing whether my setup works
print(example)

# okay, so I get monthly entries of something for every month from 1955 till 2025_03_01

# the main methods for FRED are:
# """
# fred.search("search term")
# fred.get_series("ID")
# fred.get_series_info("ID")
# """

print(client.get_series_info("DEUCPIALLMINMEI"))

# okay, so this is a CPI index, monthly, 2015 as base year
# this means every other number is a relative price expression compared to 2015

#----- Writing necessary data to CSV for local analysis

import pandas as pd

path = "./data/fred.csv"
example.to_csv(path)

df = pd.read_csv(path)
print(df.head())
