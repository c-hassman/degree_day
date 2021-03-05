#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLEAN OBSERVED

PURPOSE: Clean raw observed degree day data, collected from NOAA using 
    pull_observed.py. Produces a clean dataframe with is the written as a 
    pickle
    
    
Created on Fri Feb 26 15:10:31 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""
import logging
import os
import numpy as np
import pandas as pd
os.chdir("/home/colburn/Documents/degree_day/Database/Actual")

def clean_actual_df(filename):
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
    actual_df = pd.read_csv(filename, delimiter = "|", header = 3,na_values=-9999)
    actual_df = actual_df.set_index("Region")
    actual_df = actual_df.T
    actual_df.index = actual_df.index.rename("Date")

    actual_df.index = pd.to_datetime(actual_df.index, yearfirst = True)
    return actual_df

def merge_dd_actual(old_df, new_df):
    data = old_df.append(new_df)
    data.sort_index(inplace = True)
    return data

def main():
    logging.basicConfig(filename = "clean_actual.log", filemode="w",
                            level=logging.INFO,
                        format="%(levelname)s: %(asctime)s: %(message)s")
   
    logging.info("Program Start")
    
    years = [] # create and populate list of years as strings
    for i in range(4,22):
        yy = str("{:02d}".format(i))
        year = "20" + yy
        years.append(year)
        
    # First Heating:
    logging.info("Beginning Heating")
    HDD_df = pd.DataFrame()
    for year in years:
        logging.info("Cleaning Heating {}".format(year))
        filename = "raw_data/" + "{}_Heating".format(year)
        data = clean_actual_df(filename)
        HDD_df = merge_dd_actual(HDD_df, data)
        
    logging.info("Writing Heating")
    HDD_df.to_pickle("HDD_Observed.pkl")
    
    # Second Cooling:
    logging.info("Beginning Cooling")
    CDD_df = pd.DataFrame()
    for year in years:
        logging.info("Cleaning Cooling {}".format(year))
        filename = "raw_data/" + "{}_Cooling".format(year)
        data = clean_actual_df(filename)
        CDD_df = merge_dd_actual(CDD_df, data)
        
    logging.info("Writing Heating")
    CDD_df.to_pickle("CDD_Observed.pkl")
    
    
if __name__=="__main__":
    main()