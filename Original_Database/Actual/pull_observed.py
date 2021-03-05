#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PULL OBSERVED 

PURPOSE: Pull observed degree day data from NOAA database and store locally. 
    Follows simple design as PULL FORECASTS
    
Created on Fri Feb 26 14:40:25 2021
@author: Colburn Hassman
@contact: colburn7@vt.edu
"""


import os
os.chdir("/home/colburn/Documents/degree_day/Database/Actual")
#os.chdir("/home/ubuntu/Documents/")
import logging
from ftplib import FTP




def main():
    logging.basicConfig(filename = "pull_observed.log", filemode="w",
        level=logging.INFO,format="%(levelname)s: %(asctime)s: %(message)s")
    logging.info("Program Start")
    try:
        ftp = FTP('ftp.cpc.ncep.noaa.gov')
        ftp.login(user = "anonymous", passwd='colburn7@vt.edu')
        logging.info("Connected to FTP Server")
    except:
        logging.error("Failed to connect to FTP Server")
        print("Failed to connect to FTP Server")
      
    years = [] # create and populate list of years as strings
    for i in range(4,22):
        yy = str("{:02d}".format(i))
        year = "20" + yy
        years.append(year)
    
    # First Do Heating
    ftp.cwd("/htdocs/degree_days/weighted/daily_data/")
    data_name = "StatesCONUS.Heating.txt"
    for year in years:
        ftp.cwd("/htdocs/degree_days/weighted/daily_data/")
        logging.info("Pulling Heating Data for {}".format(year))
        file_url = year #on NOAA website
        file_name = "raw_data/"+year+"_Heating"
        file = open(file_name, 'wb')
        print(ftp.pwd())
        ftp.cwd(file_url)
        print(ftp.pwd())
        ftp.retrbinary('RETR {}'.format(data_name), file.write)
        file.close()
        
    # Second is Cooling
    ftp.cwd("/htdocs/degree_days/weighted/daily_data/")
    data_name = "StatesCONUS.Cooling.txt"
    for year in years:
        ftp.cwd("/htdocs/degree_days/weighted/daily_data/")
        logging.info("Pulling Cooling Data for {}".format(year))
        file_url = year #on NOAA website
        file_name = "raw_data/"+year+"_Cooling"
        file = open(file_name, 'wb')
        print(ftp.pwd())
        ftp.cwd(file_url)
        print(ftp.pwd())
        ftp.retrbinary('RETR {}'.format(data_name), file.write)
        file.close()
    ftp.close()
    logging.info("Program Complete")
    
if __name__ == "__main__":
    main()