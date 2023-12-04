import glob
import subprocess
import numpy as np
import os 

perc = 95
model = "GFDL-ESM4"
scenario = "historical"

y0 = 1990
y1 = 2014

def get_names(model,scenario, y0, y1):
    varn = "tasmax"
    dire = f"/media/aschrapffer/T7/DATA/NEX-GDDP/download_NEX-GDDP/Output/{model}/{scenario}/{varn}/{varn}*"
    
    g = glob.glob(dire)[0]
    basename = g.split("_")[:-1]
    basename = "_".join(basename) + "_"
    
    gg = [basename + f"{y}.nc" for y in np.arange(y0,y1+1)]
    out_name = f"{model}_{scenario}_{varn}_{y0}_{y1}.nc"
    return out_name, gg
    
def process_hd35(model,scenario, y0, y1, perc = 95):
    varn = "tasmax"
    out_name, gg = get_names(model,scenario, y0, y1)
    
    ###################
    
    subprocess.check_call(f"cdo mergetime {' '.join(gg)} temp/{out_name}", shell = True)
    
    subprocess.check_call(f"cdo gtc,308.15 temp/{out_name} temp/temp.nc", shell = True)
    subprocess.check_call(f"rm temp/{out_name}", shell = True)
       
    subprocess.check_call(f"cdo yearsum temp/temp.nc temp/temp2.nc", shell = True)
    subprocess.check_call(f"rm temp/temp.nc", shell = True)
    
    subprocess.check_call(f"cdo timavg temp/temp2.nc Output/{out_name.replace('.nc', 'mean_annual_hd35.nc')}", shell = True)
    subprocess.check_call(f"rm temp/temp2.nc", shell = True)


def get_periods(scenario):
    if scenario == "historical":
        return [1990],[2014]
    else:
        return [2020,2041],[2040,2060]

models = ["GFDL-ESM4","IPSL-CM6A-LR","MRI-ESM2-0","UKESM1-0-LL", "MPI-ESM1-2-HR"]
    
for model in models:
    print(model)
    for scenario in ["historical", "ssp245", "ssp585"]:
        print(scenario)
        Ly0, Ly1 = get_periods(scenario)
        for y0,y1 in zip(Ly0,Ly1):
            # check if exists: get name 
            out_name, gg = get_names(model,scenario, y0, y1)
            if not os.path.isfile(f"Output/{out_name.replace('.nc', 'mean_annual_hd35.nc')}"):
                process_hd35(model,scenario, y0, y1, perc = 95)
            
            
