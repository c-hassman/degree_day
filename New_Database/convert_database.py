#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONVERT DATABASE

PURPOSE: Convert the database from the original NOAA format to a format which
    Dr. Massa suggests

Created on Fri Feb 26 19:31:16 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""

import pandas as pd
import os 
os.chdir("/home/colburn/Documents/degree_day/New_Database/")


def adjust_observed(filename):
    data = pd.read_pickle(filename)
    states = data.columns
    data['Date'] = data.index
    n_data = pd.melt(data, id_vars="Date", value_vars= states)
    n_data = n_data.set_index(["Region", "Date"])
    return n_data



def adjust_forecasted(filename):
    data = pd.read_pickle(filename)
    fore_date = ["T+0", "T+1", "T+2", "T+3", "T+4", "T+5", "T+6"]
    
    data["Region"] = data.index.get_level_values(0)
    data["Date_of_F"] = data.index.get_level_values(1)
    
    data = pd.melt(data, id_vars = ["Region", "Date_of_F"], 
                           value_vars= fore_date)
    data['Date_of_F'] = pd.to_datetime(data['Date_of_F'], yearfirst=True)

    new_data = pd.DataFrame()
    for i in range(0,7): # subset the data for each fore_date
        for_len = "T+{}".format(i)
        temp_df = data[data['variable'] == for_len]
        temp_df['F_Date'] = pd.to_datetime(temp_df['Date_of_F'],
                                       yearfirst=True) + pd.DateOffset(i)
        new_data = new_data.append(temp_df)
        new_data.sort_index(inplace = True)
    
    # now I will determine t: should be t-1, t-2, ... , t-7
    new_data['t'] = new_data['variable'].str.strip().str[-1] 
    new_data['t']= new_data['t'].astype("int32")
    new_data['t']= new_data['t'].add(1)
    new_data['t']= new_data['t'].mul(-1)

    # Now I drop unnecessary assignments
    new_data = new_data.drop(["Date_of_F", 'variable' ], axis = 1)

    # Now I will set multiindex
    new_data = new_data.pivot_table(index = ['Region', "F_Date"], columns = ['t'] , values = 'value')

    # rename columns
    cols = []
    for i in new_data.columns:
        c = "t{}".format(i)
        cols.append(c)
    new_data.columns = cols        
        
    return new_data

def main():
    CDD_fore = adjust_forecasted("/home/colburn/Documents/degree_day/Original_Database/Forecasts/CDD_Forecasts.pkl")
    HDD_fore = adjust_forecasted("/home/colburn/Documents/degree_day/Original_Database/Forecasts/HDD_Forecasts.pkl")

    CDD_obs = adjust_observed("/home/colburn/Documents/degree_day/Original_Database/Actual/CDD_Observed.pkl")
    HDD_obs = adjust_observed("/home/colburn/Documents/degree_day/Original_Database/Actual/HDD_Observed.pkl")

    CDD_fore['T'] = CDD_obs['value']
    HDD_fore['T'] = HDD_obs['value']
    
    CDD_fore.to_pickle("Cooling.pkl")
    HDD_fore.to_pickle("Heating.pkl")


if __name__ == "__main__":
    main()