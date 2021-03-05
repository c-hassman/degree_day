#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STYLZED GRAPH

PURPOSE: Create a stylzed graph which illustrated the relationship between
    average temperature and Degree Days
    
Created on Wed Mar  3 15:07:06 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""

import pandas as pd
import os
os.chdir("/home/colburn/Documents/degree_day/New_Database/summary_statistics/")

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0,4*np.pi,0.1)   # start,stop,step
y = (np.sin(x)*30) + 65

CDD = y-65
for i in range(len(CDD)):
    if CDD[i] < 0:
        CDD[i] = 0

HDD = 65-y
for i in range(len(HDD)):
    if HDD[i] < 0:
        HDD[i] = 0

fig, ax = plt.subplots(2)
fig.suptitle('Average Temperature and Degree Days')

ax[0].plot(x,y,
           label = "Avg Daily Temp",
           color = "dodgerblue")
ax[0].set(ylabel = "Avg Daily Temp")
ax[0].axhline(y = 65, color = "black", linewidth = 1,
              linestyle = "--")
ax[0].axes.get_xaxis().set_ticks([])

ax[1].plot(x,CDD,
           label = "CDD",
           color = "orangered")
ax[1].plot(x, HDD,
           label = "HDD", 
           color = "dodgerblue")
ax[1].legend()
ax[1].set(ylabel = "Degree Days")
ax[1].axes.get_xaxis().set_ticks([])
plt.show()
