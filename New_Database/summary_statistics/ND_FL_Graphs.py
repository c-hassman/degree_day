#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(N)EW (Y)ORK AND (FL)ORIDA HDD AND CDD GRAPHS

Actually, changing to New York

PURPOSE: Makes a graph of degree days for North Dakota and Florida overtime,
    demonstrating the variability between states

Created on Wed Mar  3 13:54:10 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""

import pandas as pd
import os 
os.chdir("/home/colburn/Documents/degree_day/New_Database/summary_statistics/")
import matplotlib.pyplot as plt


CDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Cooling.pkl")
HDD = pd.read_pickle("/home/colburn/Documents/degree_day/New_Database/Heating.pkl")

# Subset by State
NY_CDD = CDD.loc['NY']
FL_CDD = CDD.loc['FL']

NY_HDD = HDD.loc['NY']
FL_HDD = HDD.loc['FL']

# Subset by date 
NY_CDD = NY_CDD.loc['2017-01-01':'2021-01-01']
FL_CDD = FL_CDD.loc['2017-01-01':'2021-01-01']

NY_HDD = NY_HDD.loc['2017-01-01':'2021-01-01']
FL_HDD = FL_HDD.loc['2017-01-01':'2021-01-01']

#print(type(HDD.index.get_level_values('F_Date')))
#print(HDD.head(10))

#plt.plot(ND_CDD['T'])

import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%b-%y')


fig, axs = plt.subplots(2)
fig.suptitle('Heating and Cooling Degree Days')

axs[0].plot(NY_CDD['T'], 
            color = "orangered",
            label = "CDDs",
            linewidth = 0.75)
axs[0].plot(NY_HDD['T'], 
            color = "dodgerblue",
            label = "HDDs",
            linewidth = 0.75)
axs[0].set(ylabel = "New York")
axs[0].legend()
axs[0].xaxis.set_major_formatter(myFmt)

axs[1].plot(FL_CDD['T'], 
            color = "orangered",
            label = "CDDs",
            linewidth = 0.75)
axs[1].plot(FL_HDD['T'], 
            color = "dodgerblue",
            label = "HDDs",
            linewidth = 0.75)
axs[1].set(ylabel = "Florida",
           ylim = (0, 60))
axs[1].legend()
axs[1].xaxis.set_major_formatter(myFmt)

fig.autofmt_xdate()