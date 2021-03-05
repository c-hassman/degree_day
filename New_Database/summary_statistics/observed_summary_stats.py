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
import matplotlib.pyplot as plt


# STYLIZED HDD and CDD



def obs_summ_stats(data):   
    '''
    This function takes in a dataframe (or subset of a dataframe) containing
    Degree Day information with columns t-7, ... T, and returns summary 
    statistics for only the forecast columns (not T)
    Mean and STD summary statistics use the count of each column to take a 
    weighted average across forecast lengths
    
    Returns list [count, mean, std, min, max]
    '''
    data = data['T'] # delete the forecasted data
    data_summ = data.describe() #get summary stats for each column
    total_count = data_summ.loc['count'] # get total number of obs
    
    results = [] # list to store results
    results.append(total_count) #  total sum of counts
      
    # Calculate weighted mean and standard deviation
    results.append(data_summ.loc['mean'])
    results.append(data_summ.loc['std'])
    
    results.append(data.median())
    # Calculate Min and Max
    results.append(data_summ.loc['min'])
    results.append(data_summ.loc['max'])
    
    return results



# By state

def obs_summ_stats_state(data):
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
        l.extend(obs_summ_stats(data.loc[state])) # add summ states
        results.append(l) # append state list to total results
        
    cols = ['State', 'Count', 'Mean', 'Std', 'Median', 'Min', 'Max']
    results_df = pd.DataFrame.from_records(results)
    results_df.columns = cols
    results_df = results_df.set_index(['State'])
    
    return results_df

CDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Cooling.pkl")
HDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Heating.pkl")

hdd_state = obs_summ_stats_state(HDD)
cdd_state = obs_summ_stats_state(CDD)

del hdd_state['Count']
del hdd_state['Min']

del cdd_state['Count']
del cdd_state['Min']

hdd_state.to_csv("HDD_Observed_Summary_Statistics")
cdd_state.to_csv("CDD_Observed_Summary_Statistics")
#%%

# Make Maps
import geopandas
states_map = geopandas.read_file('/home/colburn/Documents/degree_day/geopandas-tutorial/data/usa-states-census-2014.shp')

# Clean State map data
states_map = states_map.drop_duplicates()# drop duplicate States:
states_map = states_map[states_map.STUSPS != "DC"]# drop DC
states_map = states_map.sort_values(by = ['STUSPS'])#Order by STUSPS (abbreviation)
states_map = states_map.set_index('STUSPS')

# Add data to map data
states_map['CDD_Mean'] = cdd_state['Mean']
states_map['CDD_Max'] = cdd_state['Max']

states_map['HDD_Mean'] = hdd_state['Mean']
states_map['HDD_Max'] = hdd_state['Max']

#%%
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


fig, ax = plt.subplots(1,1)
plt.title("Average Cooling Degree Days")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
ax.set_axis_off()
states_map.plot(column = 'CDD_Mean', 
                ax = ax, 
                legend = True, 
                cax = cax,
                cmap = 'Reds',
                zorder = 2)
states_map.boundary.plot(color = "black", ax = ax, zorder = 1)
plt.tight_layout()

#%%

fig, ax = plt.subplots(1,1)
plt.title("Maximum Cooling Degree Day")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
ax.set_axis_off()
states_map.plot(column = 'CDD_Max', 
                ax = ax, 
                legend = True, 
                cax = cax,
                cmap = 'Reds',
                zorder = 2)
states_map.boundary.plot(color = "black", ax = ax, zorder = 1)
plt.tight_layout()

#%%
fig, ax = plt.subplots(1,1)
plt.title("Average Heating Degree Days")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
ax.set_axis_off()
states_map.plot(column = 'HDD_Mean', 
                ax = ax, 
                legend = True, 
                cax = cax,
                cmap = 'Blues',
                zorder = 2)
states_map.boundary.plot(color = "black", ax = ax, zorder = 1)
plt.tight_layout()


#%%
fig, ax = plt.subplots(1,1)
plt.title("Maximum Heating Degree Days")

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
ax.set_axis_off()
states_map.plot(column = 'HDD_Max', 
                ax = ax, 
                legend = True, 
                cax = cax,
                cmap = 'Blues',
                zorder = 2)
states_map.boundary.plot(color = "black", ax = ax, zorder = 1)
plt.tight_layout()