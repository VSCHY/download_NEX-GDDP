from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
import os
import time
from selenium.webdriver.common.by import By
import subprocess
import glob
import tqdm

###################

class chrome_driver:
    """
    Class to download data from the Google Cloud.
    """
    def __init__(self, dir_out):
        """
        Initialization.
        
        Input:
        - dir_out: directory where the file should be downloaded.
        """
        self.options=ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": dir_out, 
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True,}
        self.dir_out = dir_out
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')  # Last I checked this was necessary.


    def download(self):
        
        # get the corresponding url
        url = self.get_url()    
               
        # launch chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options = self.options
            )
                
        filename = url.split("/")[-1]

        # open the page
        driver.get(url)

        
        while not os.path.exists(self.dir_out + filename):
            time.sleep(1)      
        driver.close()

    def get_url(self):
        """
        Get the url of the file corresponding to a specific month.
        
        Inputs:
        - month
        - year
        """
        my_url = f"https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/NEX-GDDP-CMIP6/CESM2/ssp245/r4i1p1f1/rlds/rlds_day_CESM2_ssp245_r4i1p1f1_gn_2018.nc"
        return my_url


if __name__ == "__main__":
    chro = chrome_driver("./")
    chro.download()
