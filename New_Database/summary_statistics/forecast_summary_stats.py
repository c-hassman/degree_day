#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

SUMMARY_STATS

PURPOSE: Creates Summary Statistics for HDD, CDD, and Error


Created on Wed Mar  3 08:31:54 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""
# Setup

import pandas as pd
import os 
os.chdir("/home/colburn/Documents/degree_day/New_Database/summary_statistics/")
import matplotlib.pyplot as mpl


# STYLIZED HDD and CDD



def fore_summ_stats(data):   
    '''
    This function takes in a dataframe (or subset of a dataframe) containing
    Degree Day information with columns t-7, ... T, and returns summary 
    statistics for only the forecast columns (not T)
    Mean and STD summary statistics use the count of each column to take a 
    weighted average across forecast lengths
    
    Returns list [count, mean, std, min, max]
    '''
    del data['T'] # delete the observed data
    data_summ = data.describe() #get summary stats for each column
    total_count = data_summ.loc['count'].sum() # get total number of obs
    
    results = [] # list to store results
    results.append(total_count) #  total sum of counts
      
    # Calculate weighted mean and standard deviation
    cols = ['t-7','t-6','t-5','t-4','t-3','t-2','t-1']
    stats = ['mean','std']
    for stat in stats:
        temp = 0
        for col in cols:
            stat_i = data_summ[col].loc[stat]
            weight = data_summ[col].loc['count'] / total_count
            temp = temp + (stat_i * weight)
        results.append(temp)

    # Calculate Min and Max
    results.append(data_summ.loc['min'].min())
    results.append(data_summ.loc['max'].max())
    
    return results


# By state

def fore_summ_stats_state(data):
    """
    Takes in a dataframe formatted in the typical degree day format, uses 
    fore_summ_stats to calculate summary stats for each state. Returns DF of
    data
    """
    states = list(data.index.unique(level = 0)) # get list of all 48 states 
    
    results = [] # list which stores lists 
    for state in states:
        l = [] # list for state results
        l.append(str(state)) # add name of state
        l.extend(fore_summ_stats(data.loc[state])) # add summ states
        results.append(l) # append state list to total results
        
    cols = ['State', 'Count', 'Mean', 'Std', 'Min', 'Max']
    results_df = pd.DataFrame.from_records(results)
    results_df.columns = cols
    results_df = results_df.set_index(['State'])
    
    return results_df

CDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Cooling.pkl")
HDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Heating.pkl")

hdd_state = fore_summ_stats_state(HDD)
cdd_state = fore_summ_stats_state(CDD)

del hdd_state['Count']
del hdd_state['Min']

del cdd_state['Count']
del cdd_state['Min']

hdd_state.to_csv("HDD_Forecast_Summary_Statistics")
cdd_state.to_csv("CDD_Forecast_Summary_Statistics")



# Error