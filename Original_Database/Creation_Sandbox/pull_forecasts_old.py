#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 11:52:54 2021

@author: colburn
"""
#import logging
#logging.basicConfig(filename='pull_forecasts.log',level=logging.DEBUG)
import pandas as pd
import numpy as np
import os
os.chdir("/home/colburn/Documents/degree_day/Database/Forecasts")


def read_dd_forecast(filename, forecast_date):
    # IMPORT FORECASTS
    data = pd.read_csv(filename, delimiter= "|", header = 3, 
                       na_filter=False, dtype=np.float64, low_memory=False)
    
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

def merge_dd_forecasts(old_df, new_df):
    data = old_df.append(new_df)
    data.sort_index(inplace = True)
    return data

# DEFINE MONTHS, YEARS, DAYS

years = ['2014', '2015', '2016', '2017', 
         '2018', '2019', '2020', '2021']

    
# DEFINE URL
base = "ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/"
forecast = "StatesCONUS.Heating.txt"

from datetime import datetime



def pull_year_forecast(year, forecast):
   # begin_message = "Program begin. Year:"+ year+ "Forecast:"+ forecast
    #logging.info(begin_message)
    #months = ["01", "02", "03","04", "05", "06",
    #          "07", "08", "09","10", "11", "12"]
    #days = []
    #for i in range(1, 32):
    #    days.append("{:02d}".format(i))
    months = ["01"]
    days = ['01', '02', '03']
    # ENGINE
    #df_dict = {} # reduces number of appends
    data_df = pd.DataFrame()
    for month in months:
        for day in days:
            try: 
                forecast_date = pd.to_datetime(year+month+day,
                                               yearfirst=True)
                url = base + year +"/" + month + '/' + day + "/" + forecast
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                #print(current_time)
               #log_mess = "Pulling forecast for" + forecast_date
                #print("logg mess")
                #logging.info(log_mess)
                print("Time:", current_time, "Forecast Date:", forecast_date)
                day_df = read_dd_forecast(url, forecast_date)
                data_df = merge_dd_forecasts(data_df, day_df)
                print(len(data_df))
                #df_dict[forecast_date] = day_df
            except pd.errors.ParserError :
                print("day not found")
                pass
            except:
                print("Something went wrong")
    #logging.info("Program Complete")
    return(data_df)


data_2020 = pull_year_forecast("2020", forecast)
#data_2020.to_pickle("2020_Forecasts")
#print(data_2020.head(100))

#%%


def read_dd_forecast(filename, forecast_date):
    # IMPORT FORECASTS
    data = pd.read_csv(filename, delimiter= "|", header = 3, 
                       na_filter=False,  low_memory=False)
    
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

def merge_dd_forecasts(old_df, new_df):
    data = old_df.append(new_df)
    data.sort_index(inplace = True)
    return data

import numpy as np
import pandas as pd
from datetime import datetime
base = "ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/"
forecast = "StatesCONUS.Heating.txt"

def pull_year_forecast(year, forecast):
   # begin_message = "Program begin. Year:"+ year+ "Forecast:"+ forecast
    #logging.info(begin_message)
    #months = ["01", "02", "03","04", "05", "06",
    #          "07", "08", "09","10", "11", "12"]
    #days = []
    #for i in range(1, 32):
    #    days.append("{:02d}".format(i))
    months = ["02"]
    days = ['31', '02', '03']
    # ENGINE
    #df_dict = {} # reduces number of appends
    data_df = pd.DataFrame()
    for month in months:
        for day in days:
            forecast_date = pd.to_datetime(year+month+day,
                                               yearfirst=True)
            url = base + year +"/" + month + '/' + day + "/" + forecast
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
                #print(current_time)
               #log_mess = "Pulling forecast for" + forecast_date
                #print("logg mess")
                #logging.info(log_mess)
            print("Time:", current_time, "Forecast Date:", forecast_date)
            day_df = read_dd_forecast(url, forecast_date)
            print(day_df.head())
            data_df = merge_dd_forecasts(data_df, day_df)
            print(len(data_df))
                #df_dict[forecast_date] = day_df
            
    #logging.info("Program Complete")
    return(data_df)


data_2020 = pull_year_forecast("2020", forecast)
#data_2020.to_pickle("2020_Forecasts")
#print(data_2020.head(100))

