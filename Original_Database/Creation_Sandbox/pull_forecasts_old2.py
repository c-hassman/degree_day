#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULL FORECAST

PURPOSE: Pull raw txt data from NOAA and store locally for further cleaning

Created on Wed Feb 24 14:44:20 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""

#import pandas as pd

import os
os.chdir("/home/colburn/Documents/degree_day/Database/Forecasts")
#os.chdir("/home/ubuntu/Documents/")
import logging
from ftplib import FTP



def pull_degree_ts(url, name):
   # url_data = urlopen(url)
    file = open(name, 'w')
    for line in url_data:
        file.write(str(line) + '\n')
    file.close()
    logging.info("Successfully Wrote {}".format(name))
    



def main():
    logging.basicConfig(filename = "pull_forecast.log", filemode="w",
        level=logging.INFO,format="%(levelname)s: %(asctime)s: %(message)s")
   
    ftp = FTP('ftp.ncdc.noaa.gov')
    ftp.login(user = "anonymous", passwd='colburn7@vt.edu')
     
    
    # Define Days, Month, Years
    months = ["01", "02", "03","04", "05", "06",
              "07", "08", "09","10", "11", "12"]
    days = []
    for i in range(1, 32):
        days.append("{:02d}".format(i))
    years = ['2014', '2015', '2016', '2017', 
             '2018', '2019', '2020', '2021']   
    # Define things to assist with URL
    base_url = "ftp://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_forecasts_7day/"
    forecast_url = "/StatesCONUS.Heating.txt"
    for year in years:
        for month in months:
            for day in days:
                date = year+month+day
                logging.info(msg = "Pulling Forcast for {}".format(date))
                filename = "raw_data/" + date + "_Heating.txt"
                url = base_url + year + "/" + month + "/" + day + forecast_url
                wget.download(url, filename)
    
    
if __name__ == "__main__":
    main()