# BAScrape


BAScrape is a web scraping app for use with Webctrl 7.0 using Selenium

Written by: Daniel Woodson

Written on: 2024.04.11

The purpose of this app is to help collect the Temp & Rh data of our facility.

The BAS has a username and password setup specifically for this app.

You will need to create an .env file with the following variables, set appropriatly:
- USER_NAME=*the un you have set up*
- PASSWORD=*that users pw*
- BAS_URL=*the url of the bas server*
- ORIGIN_PATH=*the path where the bas downloads files, typically the 'downloads' folder*
- DESTINATION_PATH=*the path where you want the downloaded files to reside*
 
A \*.bat file can be created to use a windows scheduler. It would be something like this:

@echo off  
cd "C:\ *the location of your file* \BAScrape\"  
.\Scripts\activate  
python bascrape.py %\*  
pause  

Leaving the "pause" allows you to see errors. It can be removed if you are satisfied that things are working ok.