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
    
def process_heat_stress(model,scenario, y0, y1, perc = 95):
    varn = "tasmax"
    out_name, gg = get_names(model,scenario, y0, y1)
    
    ###################
    
    subprocess.check_call(f"cdo mergetime {' '.join(gg)} temp/{out_name}", shell = True)
    
    subprocess.check_call(f"cdo timpctl,{perc} temp/{out_name} -timmin temp/{out_name} -timmax temp/{out_name} Output/{out_name.replace('.nc', '_p95.nc')}", shell = True)
    
    
    dp95 = f"Output/{model}_historical_{varn}_1990_2014_p95.nc"
    
    subprocess.check_call(f"cdo sub temp/{out_name} Output/{out_name.replace('.nc', '_p95.nc')} temp/temp.nc", shell = True)
    subprocess.check_call(f"rm temp/{out_name}", shell = True)
    
    subprocess.check_call(f"cdo gtc,0 temp/temp.nc temp/temp2.nc", shell = True)
    subprocess.check_call(f"rm temp/temp.nc", shell = True)
    

    subprocess.check_call(f"cdo yearsum temp/temp2.nc temp/temp3.nc", shell = True)
    subprocess.check_call(f"rm temp/temp2.nc", shell = True)

    subprocess.check_call(f"cdo timavg temp/temp3.nc Output/{out_name.replace('.nc', '_days_above_p95.nc')}", shell = True)
    subprocess.check_call(f"rm temp/temp3.nc", shell = True)


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
            if not os.path.isfile(f"Output/{out_name.replace('.nc', '_days_above_p95.nc')}"):
                process_heat_stress(model,scenario, y0, y1, perc = 95)
            
            
