import glob
import xarray as xr
import numpy as np

import matplotlib.pyplot as plt

nlat = 600
nlon = 1440

scenarios = ["historical", "ssp245", "ssp585"]
Dperiods = {"hist":"1990_2014", "2030":"2020_2040", "2050":"2041_2060"}
Dscenar = {"historical":["hist"], "ssp245":["2030","2050"], "ssp585":["2030","2050"]}

############# 
# p95      
D_p95 = {}
for scenario in scenarios:

    periods = Dscenar[scenario]
    
    for period in periods:
        data = np.ma.zeros((5,nlat,nlon))

        gg = glob.glob(f"Output/*{scenario}*{Dperiods[period]}_p95*")
        for i, g in enumerate(gg):

            ds = xr.open_dataset(g)
            if i == 0:
                lon = ds.coords["lon"]
                lat = ds.coords["lat"]
            
            d = ds["tasmax"][0,:,:].values
            xmask=np.isnan(d)
            d = np.ma.masked_where(xmask, d)
            data[i,:,:] = d-273.15

        data = np.ma.median(data, axis = 0)
        
        D_p95[f"p95_median_{scenario}_{period}"] = xr.DataArray(
                          data   = data,
                          dims   = ['lat',"lon"],
                          coords = {'latitude':lat,"longitude":lon}) 
        

ds = xr.Dataset(D_p95)
ds.to_netcdf("Processed/p95.nc")

############# 
# Increase days # % ?? or Number of days

D_days_p95 = {}

for scenario in scenarios:
    periods = Dscenar[scenario]
    
    for ip, period in enumerate(periods):
        gg = glob.glob(f"Output/*{scenario}*{Dperiods[period]}_days_above_p95*")
        data = np.ma.zeros((5,nlat,nlon))
        for i, g in enumerate(gg):
            if ip == 0 and i == 0:
                lon = ds.coords["lon"]
                lat = ds.coords["lat"]
                        
            ds = xr.open_dataset(g)
            d = ds["tasmax"][0,:,:].values
            xmask=np.isnan(d)
            d = np.ma.masked_where(xmask, d)
            data[i,:,:] = d

        data = np.ma.median(data, axis = 0)
        
        D_days_p95[f"days_above_p95_median_{scenario}_{period}"] = xr.DataArray(
                          data   = data,
                          dims   = ['lat',"lon"],
                          coords = {'latitude':lat,"longitude":lon}) 
        
ds = xr.Dataset(D_p95)
ds.to_netcdf("Processed/days_above_p95.nc")
 
