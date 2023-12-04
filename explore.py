import requests
import pandas as pd
import numpy as np
import tqdm
import sys

url = 'https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/catalog.html'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[0]
datasets = df["Dataset"].values[1:]

Lout = []

for model in tqdm.tqdm(datasets[:]):
    D = {}
    url = f'https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/{model}/catalog.html'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[0]
    scenarios = df["Dataset"].values[1:]
    for scenario in scenarios:
        url = f'https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/{model}/{scenario}/catalog.html'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[0]

        end = df["Dataset"].values[1:]
        if len(end) == 1:
            member = end[0]
        else:
            # Check that only single member for each model
            print("Multiple member")
            sys.exit()

        url = f'https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/{model}/{scenario}/{member}/catalog.html'
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[0]
        varlist = list(df["Dataset"].values[1:])

        D = {"Model":model, "Scenario":scenario, "Member": member}
        for varn in ['hurs', 'huss', 'pr', 'rlds', 'rsds', 'sfcWind', 'tas', 'tasmax', 'tasmin']:
            if varn in varlist:
                D[varn] = 1
            else:
                D[varn] = 0
        Lout.append(D)

# Create a DataFrame
df = pd.DataFrame(Lout)
df.to_excel("Data_Available.xlsx", index = False)

# Available
# 'hurs' 'huss' 'pr' 'rlds' 'rsds' 'sfcWind' 'tas' 'tasmax' 'tasmin'

# FWI:  temperature, relative humidity, wind speed, rainfall
# 'tas', 'hurs','sfcWind','pr'

# Selection of models that (1) contains all variables for scenarios historical ssp245 et ssp585


"""
Choix de modèles:

GFDL-ESM4,      OUI
IPSL-CM6A-LR,   OUI (n'a juste pas huss, mais non nécessaire)
MPI-ESM1–2-HR,  OUI
MRI-ESM2-0,     OUI
UKESM1-0-LL     OUI
"""