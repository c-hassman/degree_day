#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sandbox

PURPOSE: 
    Build the system for database creation and validation for Degree Day 
    forecasts
    
    
Created on Tue Feb 23 14:18:49 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""

import pandas as pd
import numpy as np

# TO DO:
    # ADD LOGGING
    # ADD MORE ERRORS
    # URL loop
    # Documentation
    # Actuals 
    # error calculation handles days wwhich havent happened yet

#%%

def read_dd_forecast(filename):
    # GET DATE FORECAST WAS MADE
    with open(filename) as f: # open the txt file which contains dd forecast
        line = f.readlines(1) # read only first line of forecast
    line = list(str(line[0])) # convert first line into list of single char.
    forecast_date = line[-9:-1] # subset to contain only relevant char.
    forecast_date = pd.to_datetime("".join(forecast_date), # join list into 
                                   yearfirst= True) # str and convert to dt

    # IMPORT FORECASTS
    data = pd.read_csv(filename, delimiter= "|", header = 3)
    
    # FORMAT DATA 
    data = data.drop(columns = "Total") # drop total column
    data['Date'] = forecast_date
    data = data.set_index(['Region', 'Date'])
        
    # VALIDATE FORECAST DATES
    # Both makes sure that T+i comes i days after forecast
    # AND checks for missing or misformatted dates
    for i in range(len(data.columns)):
        c_date = pd.to_datetime(data.columns[i], # date from column
                                yearfirst = True) 
        f_date = forecast_date + np.timedelta64(i, 'D') # correct date 
        if c_date == f_date : # check if column date is correct
            pass
        else: 
            print("Forecast Date:", forecast_date)
            print("Expected: ", f_date, "Got:", c_date)
            raise ValueError("Date Error: Columns incorrect based on date of Forecast")
    
    # RENAME COLUMNS
    col_list = [] # Create list of "T_0", "T_1" ...
    for i in range(len(data.columns)):
        col_list.append("T+{}".format(i))
    data.columns = col_list # Rename columns in dataframe
    
    return data

#%%
data1 = read_dd_forecast("StatesCONUS.Heating.txt")
data2 = read_dd_forecast("StatesCONUS.Heating(1).txt")

#%%

def merge_dd_forecasts(old_df, new_df):
    data = old_df.append(new_df)
    data.sort_index(inplace = True)
    return data
    
data = merge_dd_forecasts(data1, data2)
data = merge_dd_forecasts(data, read_dd_forecast("StatesCONUS.Heating(2).txt"))

print(data.head())

            
#%%%
# THIS IS GOOD... USE THIS AND ABOVE.. MAKE INTO FUNCTION

def calculate_error(forecast_df, actual_df):
    '''
    This function calculates the error of degree day forecasts.

    Parameters
    ----------
    forecast : A dataframe of degree day forecasts. Multiindexed by Region 
        and date. Columns of T+0, T+1, ... , T+6
    actual : A dataframe with the date as the index, Regions as columns, 
        and the observed degree days as values.
    
    Returns
    -------
    error_df: A dataframe of errors between the forecast and actual given
        a specified error_function

    '''
    states = list(forecast_df.index.unique(level = 0)) # retrieve list of states
    
    # ENGINE
    # Appending to dataframe is inappropriate for this task, takes quadratic
    # time. Instead we built a list which contains lists of state data,
    # containing lists of daily data for multiple forecast time frames 
    # (3 layers of lists.) This has much better time complexity
    results = [] # initialize a list to store all results
    for state in states: # First loop does each state len(num states)
       state_results = [] # initalize list to store state results. len(num days)
       for index, row in forecast_df.loc[state].iterrows():# Second loop does each day T
           day_results = [] # Initialize list to store daily restuls len(num T)
           for T in range(len(row)): # Third loop does each forecast in day T
                #print(state, index, "T+{}".format(T), row["T+{}".format(T)]) # Place holder
                forecast = row["T+{}".format(T)]# Access forecast value
                #actual = 0 #!!!!!!!!!!!!!
                f_date = index +  np.timedelta64(T, 'D') # find the date being forecasted
                actual = actual_df.loc[f_date, state] # retrieve actual
                error = forecast - actual
                #print("State:", state, "DofF:", index,"F_date", f_date, "Fcast:", forecast, "Act:", actual, "Err:", error)
                day_results.append(error)
           state_results.append(day_results)
       results.append(state_results)
    
    # CONVERT TO DATAFRAME
    results_df = pd.DataFrame()
    for i in range(len(results)): # unpack lists of lists of lists.  Will loop len(states)
        temp_df = pd.DataFrame.from_records(results[i]) # store results for each state
        results_df = results_df.append(temp_df) # append to primary df
    
    # REBUILD INDEX
    # Create Date Index
    dates = list(forecast_df.index.unique(level = 1)) # get unique dates
    n_states = len(states)
    dates_col = list(dates * n_states)

    # Create Region Index
    region_col = []
    for state in states:
        for j in range(len(dates)):
            region_col.append(state)
            
    # Rename Columns
    col_list = [] # Create list of "T_0", "T_1" ...
    for i in range(len(forecast_df.columns)):
        col_list.append("T+{}".format(i))
    
    results_df.columns = col_list # reset column names
    results_df['Region'] = region_col # make region column
    results_df['Date'] = dates_col # make date column

    results_df = results_df.set_index(['Region', "Date"]) # set multiindex

    return results_df



# PULL ACTUAL OBSERVED
def pull_actual_df(filename):
    '''
    Takes a raw NOAA Degree day file and converts it to a well formatted
    Dataframe

    Parameters
    ----------
    filename : the location of the raw data

    Returns
    -------
    actual_df: dataframe with states as columns, dates and index,
        containing actual observed degree days

    '''
    actual_df = pd.read_csv(filename, delimiter = "|", header = 3)
    actual_df = actual_df.set_index("Region")
    actual_df = actual_df.T
    actual_df.index = actual_df.index.rename("Date")

    actual_df.index = pd.to_datetime(actual_df.index, yearfirst = True)
    return actual_df


actual_df = pull_actual_df("test_Actual.txt")

data = read_dd_forecast("test_f1.txt")
data = merge_dd_forecasts(data, read_dd_forecast("test_f2.txt"))
data = merge_dd_forecasts(data, read_dd_forecast("test_f3.txt"))


results = calculate_error(data, actual_df)

print(results)

#%%

#NOW URL time
from urllib.request import urlopen
months = ["01", "02", "03","04", "05", "06",
          "07", "08", "09","10", "11", "12"]
years = ['2014', '2015', '2016', '2017', 
         '2018', '2019', '2020', '2021']
days = []
for i in range(1, 32):
    days.append("{:02d}".format(i))

# One area to improve might be to get rid of the df append
# method in merge_dd_forecasts, as it has poort time compl.

#ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/2021/01/01/StatesCONUS.Heating.txt

base = "ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/"
forecast = "StatesCONUS.Heating.txt"

def get_nth_line(resp, n):
    i = 1
    while i < n:
        resp.readline()
        i += 1
    return resp.readline()


for month in months:
    for day in days:
        url = base + '2020/' +month + "/" + day + "/" + forecast
        print("pulling data")
        url_data = urlopen(url) #opens the url using 
        name = "2020"+month+day+"_"+forecast
        line = get_nth_line(url_data, 1)
        forecast_date = line[-8:-1]
        print(forecast_date)
        
        
#%%
def get_nth_line(resp, n):
    i = 1
    while i < n:
        resp.readline()
        i += 1
    return resp.readline()

from urllib.request import urlopen
base = "ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/"
forecast = "StatesCONUS.Heating.txt"

days = []
for i in range(1, 32):
    days.append("{:02d}".format(i))
    
for day in days:
    url = base + '2020/1/' + day + "/" + forecast
    print("pulling data")
    url_data = urlopen(url) #opens the url using 
    line = get_nth_line(url_data, 1)
    forecast_date = line[-8:-1]
    print(forecast_date)    
        
#%%


for month in months:
    for day in days:
        url = base + '2020/' +month + "/" + day + "/" + forecast
        print("pulling data")
        
        name = "2020"+month+day+"_"+forecast
        data = read_dd_forecast(url)
        print(data.head())
        
#%%
data = pd.read_csv(url, delimiter= "|", header = 3)
print(data)
        
#%%

test_df = read_dd_forecast("20200101_StatesCONUS.Heating.txt")
print(test_df)

#%%


























