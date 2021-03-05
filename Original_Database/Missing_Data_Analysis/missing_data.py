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
os.chdir("/home/colburn/Documents/degree_day/Original_Database")

import matplotlib.pyplot as plt
import numpy as np

CDD_fore = pd.read_pickle("Forecasts/CDD_Forecasts.pkl")
HDD_fore = pd.read_pickle("Forecasts/HDD_Forecasts.pkl")

#%%

# Okay here we are getting somewhere
print("Total Missing; \n", CDD_fore.isnull().sum())

print(CDD_fore.loc['AL'].isnull().sum())

#%%
cdd_total_list = list(CDD_fore.isnull().sum())
hdd_total_list = list(HDD_fore.isnull().sum())
days = ['T-1','T-2','T-3','T-4','T-5','T-6','T-7']

total_df = pd.DataFrame()
total_df["Forecast"]=days
total_df["CDD"] = cdd_total_list
total_df["HDD"] = hdd_total_list
#%%


x = np.arange(len(days))
width = 0.35

fig, ax = plt.subplots()
cdd_bar = ax.bar(x - width/2, cdd_total_list, width, label = "CDD", 
                 color = "orangered")
hdd_bar = ax.bar(x + width/2, hdd_total_list, width, label = "HDD",
                 color = "dodgerblue")

ax.set_ylabel('Missing Data Count')
ax.set_title('Missing Data by Forecast Length')
ax.set_xticks(x)
ax.set_xticklabels(days)
ax.legend()

plt.show()

#%%
per_cdd_total_list = list(CDD_fore.isnull().sum()/(len(CDD_fore))*100)
per_hdd_total_list = list(HDD_fore.isnull().sum()/(len(HDD_fore))*100)
days = ['T-1','T-2','T-3','T-4','T-5','T-6','T-7']

per_total_df = pd.DataFrame()
per_total_df["Forecast"]=days
per_total_df["CDD"] = per_cdd_total_list
per_total_df["HDD"] = per_hdd_total_list



x = np.arange(len(days))
width = 0.35

fig, ax = plt.subplots()
cdd_bar = ax.bar(x - width/2, per_cdd_total_list, width, label = "CDD", 
                 color = "orangered")
hdd_bar = ax.bar(x + width/2, per_hdd_total_list, width, label = "HDD",
                 color = "dodgerblue")

ax.set_ylabel('Percent Missing Data (%)')
ax.set_title('Missing Data by Forecast Length')
ax.set_xticks(x)
ax.set_xticklabels(days)
ax.legend()

plt.show()

#%%
#print(CDD_fore["2014-01-01": "2021-12-31"].isnull().sum())

dateindex = CDD_fore.index.get_level_values('Date')
cdd_dateindex = pd.DatetimeIndex(dateindex)

dateindex = HDD_fore.index.get_level_values('Date')

hdd_dateindex = pd.DatetimeIndex(dateindex)
#%%

print(CDD_fore.loc[cdd_dateindex.year == 2017].isnull().sum().sum())

#%%
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
cdd_miss_year = []
hdd_miss_year = []

for year in years:
    cdd_miss = CDD_fore.loc[cdd_dateindex.year == year].isnull().sum().sum() / (len(CDD_fore.loc[cdd_dateindex.year == year]) * 7) * 100
    cdd_miss_year.append(cdd_miss)
    hdd_miss = HDD_fore.loc[hdd_dateindex.year == year].isnull().sum().sum() / (len(HDD_fore.loc[hdd_dateindex.year == year]) * 7) * 100
    hdd_miss_year.append(hdd_miss)
    
#%%
x = np.arange(len(years))
width = 0.35

fig, ax = plt.subplots()
cdd_bar = ax.bar(x - width/2, cdd_miss_year, width, label = "CDD", 
                 color = "orangered")
hdd_bar = ax.bar(x + width/2, hdd_miss_year, width, label = "HDD",
                 color = "dodgerblue")

year_labels = ['2014','2015','2016','2017','2018','2019','2020', '2021*' ]

ax.set_ylabel('Percent Missing Data (%)')
ax.set_title('Missing Data by Year')
ax.set_xticks(x)
ax.set_xticklabels(year_labels)
ax.legend()

txt = "* 2021 only includes up to February 24"
fig.text(.5, .02, txt, ha='left')

plt.show()
#%%

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
cdd_miss_month = []
hdd_miss_month = []

for month in months:
    cdd_miss = CDD_fore.loc[cdd_dateindex.month == month].isnull().sum().sum()/ (len(CDD_fore.loc[cdd_dateindex.month == month]) * 7) * 100
    cdd_miss_month.append(cdd_miss)
    hdd_miss = HDD_fore.loc[hdd_dateindex.month == month].isnull().sum().sum()/ (len(HDD_fore.loc[hdd_dateindex.month == month]) * 7) * 100
    hdd_miss_month.append(hdd_miss)
    
    #%%
month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", 
              "Sep", "Oct", "Nov", "Dec"]
x = np.arange(len(months))
width = 0.35

fig, ax = plt.subplots()
cdd_bar = ax.bar(x - width/2, cdd_miss_month, width, label = "CDD", 
                 color = "orangered")
hdd_bar = ax.bar(x + width/2, hdd_miss_month, width, label = "HDD",
                 color = "dodgerblue")

ax.set_ylabel('Percentage Missing Data (%)')
ax.set_title('Missing Data by Month')
ax.set_xticks(x)
ax.set_xticklabels(month_abbr)
ax.legend()

plt.show()
#%%
import geopandas
states = geopandas.read_file('/home/colburn/Documents/degree_day/geopandas-tutorial/data/usa-states-census-2014.shp')

#%%

states.plot()

#%%
states.boundary.plot()
#%%

fig = plt.figure(1, figsize=(25,15)) 
ax = fig.add_subplot()

states.apply(lambda x: ax.annotate(s=x.NAME, xy=x.geometry.centroid.coords[0], ha='center', fontsize=14),axis=1);
states.boundary.plot(ax=ax, color='Black', linewidth=.4)
states.plot(ax=ax, cmap='Pastel2', figsize=(12, 12))

plt.show()

#%%

# drop duplicate States:
states = states.drop_duplicates()
# drop DC
states = states[states.STUSPS != "DC"]

#Order by STUSPS (abbreviation)
states = states.sort_values(by = ['STUSPS'])

#%%
# make list of states
states_abbr = list(CDD_fore.index.unique(level = 0))

state_index = CDD_fore.index.get_level_values('Region')
# calculate missing values for each state:
state_list = []
for state in states_abbr:
    temp = CDD_fore.loc[state_index == state].isnull().sum().sum()
    state_list.append(temp)
    
    
# add CDD missing values to states 
#%%
AL_df = CDD_fore.loc["AL"]
WI_df = CDD_fore.loc['WI']
print(AL_df.isnull().sum().sum())


#%%

fig = plt.figure(1, figsize=(25,15)) 
ax = fig.add_subplot()































