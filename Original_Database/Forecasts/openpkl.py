#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:30:03 2021

@author: colburn
"""

import pandas as pd

import os
os.chdir("/home/colburn/Documents/degree_day/Database/Forecasts")

data = pd.read_pickle("CDD_Forecasts.pkl")

#%%
data = pd.read_csv("raw_data/20140101_Heating.txt", delimiter = "|",
                   header = 3)