#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MISSING DATA ANALYSIS

PURPOSE: This script is to investigate the missing data found in the forecast
    and actual degree day datasets

Not super clean... but OKAY

Done on original forecasts with -9999 as NA

Created on Thu Feb 25 17:34:51 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""
import pandas as pd
import os
os.chdir("/home/colburn/Documents/degree_day/Database")

CDD_fore = pd.read_pickle("Forecasts/CDD_Forecasts.pkl")
HDD_fore = pd.read_pickle("Forecasts/HDD_Forecasts.pkl")


### Should approache this differently. Calculate and store a dataframe of 0 and 1
# where 1s are -9999. Go from there. 




CDD_miss = CDD_fore[CDD_fore.eq(-9999)].any(1)
print("CDD: Number of forecasts with at least one missing value:", sum(CDD_miss))
print("CDD: Percent of forcasts with at least one missing value:", round(sum(CDD_miss)/len(CDD_fore)*100, 6))

CDD_missing = CDD_fore.where(CDD_fore == -9999).dropna() # belive this is row based
print("CDD: Number of Forecasts where all values are missing:", len(CDD_missing))
print("CDD: Percent of Forecasts where all values are missing:", round(len(CDD_missing)/len(CDD_fore)*100, 6))

HDD_miss = HDD_fore[HDD_fore.eq(-9999)].any(1)
print("HDD: Number of forecasts with at least one missing value:", sum(HDD_miss))
print("HDD: Percent of forcasts with at least one missing value:", round(sum(HDD_miss)/len(HDD_fore)*100, 6))

HDD_missing = HDD_fore.where(HDD_fore == -9999).dropna() # belive this is row based
print("HDD: Number of Forecasts where all values are missing:", len(HDD_missing))
print("HDD: Percent of Forecasts where all values are missing:", round(len(HDD_missing)/len(HDD_fore)*100, 6))



CDD_dict = {}
for i in range(0,6):
    t = "T+"+str(i)
    df_name = str("CDD_T" + str(i))
    temp_df = CDD_fore[CDD_fore[t] ==  -9999]
    CDD_dict[df_name] = temp_df
    
HDD_dict = {}
for i in range(0,6):
    t = "T+"+str(i)
    df_name = str("HDD_T" + str(i))
    temp_df = HDD_fore[HDD_fore[t] ==  -9999]
    HDD_dict[df_name] = temp_df
    
#%%


