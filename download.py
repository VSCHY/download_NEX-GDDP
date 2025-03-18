import requests
import pandas as pd
import numpy as np
import tqdm
import sys
import subprocess
import os
import time

############################################

def get_years(scenario):
    if scenario == "historical":
        y0 = 1990
        y1 = 2014
        first = 1950
    elif scenario == "ssp585":
        y0 = 2015
        y1 = 2100
        first = 2015
    elif scenario == "ssp245":
        y0 = 2015
        y1 = 2100
        first = 2015
    return first, y0, y1

############################################

def create_directory(dire):  
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    if not os.path.exists(f"{dir_path}/{dire}/"):
        subprocess.check_call(f"mkdir {dir_path}/{dire}", shell = True)

############################################

class NEX_GDDP:
    def __init__(self):
        self.df = pd.read_excel("./Data_Available.xlsx")
        self.base_cmd = "wget https://ds.nccs.nasa.gov/thredds/fileServer/AMES/NEX/GDDP-CMIP6/"
        
    def get_url(self):
        self.url = f"https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/{self.model}/{self.scenario}/{self.member}/{self.varname}/catalog.html"
        
        
    def clean_up(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        subprocess.check_call(f"rm {dir_path}/*.nc", shell = True)
        
    def set_env(self, model, scenario, varname):
        self.model = model
        self.scenario = scenario
        self.varname = varname
        self.first, self.y0, self.y1 = get_years(scenario)   
             
        df_t = self.df[self.df["Model"] == model]
        df_t = df_t[df_t["Scenario"] == scenario]

        if df_t.shape[0] != 1:
            print(df_t)
            print(self.df["Model"].unique())
            print("ERROR")
            sys.exit()
        
        self.member = df_t["Member"].iloc[0]        

        create_directory(f"Output")
        create_directory(f"Output/{model}/")
        create_directory(f"Output/{model}/{scenario}/")
        create_directory(f"Output/{model}/{scenario}/{varname}/")

    def download(self, model, scenario, varname):
        #self.clean_up()
        self.set_env(model, scenario, varname)
        #
        self.get_url()
        time.sleep(0.2)
        #
        html = requests.get(self.url).content
        df_list = pd.read_html(html)
        #
        base = df_list[0]["Dataset"].iloc[0]
        filename = df_list[0]["Dataset"].iloc[1].replace(str(self.first), "{0}")
        #
        if varname == "hurs":
            filename = filename.replace(".nc","_v1.1.nc")
        #
        cmd = self.base_cmd + base + filename
        for y in range(self.y0, self.y1+1):
            if not os.path.exists(f"Output/{model}/{scenario}/{varname}/{filename.format(y)}"):
                subprocess.check_call(cmd.format(y), shell = True)
                subprocess.check_call(f"mv {filename.format(y)} Output/{model}/{scenario}/{varname}", shell = True)
        

