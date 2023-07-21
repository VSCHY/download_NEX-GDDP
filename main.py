from src import *

dir_out = '/media/anthony/easystore/GSWD_Pampa/Originals/'
ch_dr = chrome_driver(dir_out)

for year in range(2000,2022):
    for month in range(1,13):     
        ch_dr.download(year,month)
