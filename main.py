from download import NEX_GDDP


nxgddp = NEX_GDDP()

varname = "tasmax"        


#DONE : "tasmax", "tas", "tasmin","pr","sfcWind", "hurs"
#FOR LATER "rlds","rsds"

# ["historical", "ssp585", "ssp245"]
# ["GFDL-ESM4", "IPSL-CM6A-LR", "MPI-ESM1-2-HR", "MRI-ESM2-0", "UKESM1-0-LL"]

#"hurs" download _1_1 -> check in different models

variables_name = ["rsds"]

for varname in variables_name:
    print(varname)
    for scenario in ["historical", "ssp585", "ssp245"]:
        print(scenario)
        for model in ["GFDL-ESM4", "IPSL-CM6A-LR", "MPI-ESM1-2-HR", "MRI-ESM2-0", "UKESM1-0-LL"]:
            print(model)
            nxgddp.download(model, scenario, varname)


