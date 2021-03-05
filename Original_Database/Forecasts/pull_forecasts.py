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



def main():
    logging.basicConfig(filename = "pull_forecast.log", filemode="w",
        level=logging.INFO,format="%(levelname)s: %(asctime)s: %(message)s")
   
    logging.info("Program Start")
    try:
        ftp = FTP('ftp.cpc.ncep.noaa.gov')
        ftp.login(user = "anonymous", passwd='colburn7@vt.edu')
        logging.info("Connected to FTP Server")
    except:
        logging.error("Failed to connect to FTP Server")
        print("Failed to connect to FTP Server")
     
    
    # Define Days, Month, Years
    months = ["01", "02", "03","04", "05", "06",
              "07", "08", "09","10", "11", "12"]
    days = []
    for i in range(1, 32):
        days.append("{:02d}".format(i))
    years = ['2014', '2015', '2016', '2017', 
             '2018', '2019', '2020', '2021']   
      
    # First Do Heating
    ftp.cwd("/htdocs/degree_days/weighted/daily_forecasts_7day")
    forecast_name = "StatesCONUS.Heating.txt"
    for year in years:
        for month in months:
            for day in days:
                ftp.cwd("~/htdocs/degree_days/weighted/daily_forecasts_7day")
                date = year+month+day
                logging.info(msg = "Pulling Forcast for {}".format(date))
                filename = "raw_data/" + date + "_Heating.txt"
                ftp_url =  year + "/" + month + "/" + day 
                           
                # Open File
                try:
                    file = open(filename, 'wb')
                    ftp.cwd(ftp_url)
                    ftp.retrbinary('RETR {}'.format(forecast_name), file.write)
                    file.close()
                    print("Sucessfully download Heating", date)
                    logging.info("Sucessfully download Heating {}".format(date))
                except:
                    logging.info("Skipped Day: {}".format(date))
                    pass
                
    # Second to Cooling
    ftp.cwd("/htdocs/degree_days/weighted/daily_forecasts_7day")
    forecast_name = "StatesCONUS.Cooling.txt"
    for year in years:
        for month in months:
            for day in days:
                ftp.cwd("~/htdocs/degree_days/weighted/daily_forecasts_7day")
                date = year+month+day
                logging.info(msg = "Pulling Forcast for {}".format(date))
                filename = "raw_data/" + date + "_Cooling.txt"
                ftp_url =  year + "/" + month + "/" + day 
                print(ftp.pwd())
                
                
                # Open File
                try: 
                    file = open(filename, 'wb')
                    ftp.cwd(ftp_url)
                    ftp.retrbinary('RETR {}'.format(forecast_name), file.write)
                    file.close()
                    print("Sucessfully download ", date)
                    logging.info("Successfully downloaded Cooling {}".format(date))
                except:
                    logging.info("Skipped Day: {}".format(date))
                    pass
                
    ftp.close()
    logging.info("Program Finished")
    
    
if __name__ == "__main__":
    main()