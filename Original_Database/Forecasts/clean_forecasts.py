#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLEAN FORECAST.PY

PURPOSE: Reads in all Degree Day Forecasts stored in raw_data/. Cleans and 
    formats data into a single dataframe and stores it as a pickle file

Created on Wed Feb 24 20:42:00 2021
@author: Colburn Hassman
@contract: colburn7@vt.edu
"""
import logging
import os
import numpy as np
import pandas as pd
os.chdir("/home/colburn/Documents/degree_day/Database/Forecasts")


def read_dd_forecast(filename, forecast_date):
    # IMPORT FORECASTS
    data = pd.read_csv(filename, delimiter= "|", header = 3,na_values=-9999)
                      
    
    # FORMAT DATA 
    data = data.drop(columns = "Total") # drop total column
    data['Date'] = forecast_date
    data = data.set_index(['Region', 'Date'])
    
    forecast_date = pd.to_datetime(forecast_date, yearfirst=True)
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

def main():
    logging.basicConfig(filename = "clean_forecast.log", filemode="w",
                        level=logging.INFO,
                        format="%(levelname)s: %(asctime)s: %(message)s")
   
    logging.info("Program Start")
    # Define Time
    years = ['2014', '2015', '2016', '2017', 
         '2018', '2019', '2020', '2021']
    months = ["01", "02", "03","04", "05", "06",
              "07", "08", "09","10", "11", "12"]
    days = []
    for i in range(1, 32):
        days.append("{:02d}".format(i))
    
    # Heating First
    heating_df = pd.DataFrame()
    for year in years:
        for month in months:
            for day in days:
                date = year+month+day
                filename ="raw_data/"+date+"_Heating.txt"
                
                try:
                    new_df = read_dd_forecast(filename, date)
                    heating_df = merge_dd_forecasts(heating_df, new_df)
                    print("Added Forecast: {}".format(date))
                    logging.info("Added Forecast: {}".format(date))
                except:
                    logging.info("Skipping {}".format(date))
                    pass
    heating_df.to_pickle("HDD_Forecasts.pkl")
    logging.info("Successfully Wrote Heating DF")
    print("Successfully Wrote Heating DF")
    # Cooling Second
    cooling_df = pd.DataFrame()
    for year in years:
        for month in months:
            for day in days:
                date = year+month+day
                filename ="raw_data/"+ date+"_Cooling.txt"
                try:
                    new_df = read_dd_forecast(filename, date)
                    cooling_df = merge_dd_forecasts(cooling_df, new_df)
                    print("Added Forecast: {}".format(date))
                    logging.info("Added Forecast: {}".format(date))
                except:
                    logging.info("Skipping {}".format(date))
                    pass
    cooling_df.to_pickle("CDD_Forecasts.pkl")
    print("Successfully Wrote Cooling DF")
    logging.info("Successfully Wrote Cooling DF")

if __name__=="__main__":
    main()
