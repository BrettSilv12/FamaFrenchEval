import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Union
import requests
import io
import zipfile
from datetime import datetime
import urllib
from sklearn.linear_model import LinearRegression

class FamaFrenchDataLoader:
    def __init__(self):
        """Initialize the Fama-French data loader"""
        self.base_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp"
        
    def _download_data(self) -> pd.DataFrame:
        """
        Download and extract data from Kenneth French's website
        
        Parameters:
        file_name (str): Name of the file to download
        
        Returns:
        pd.DataFrame: Extracted data
        """
        url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
        try:
            with urllib.request.urlopen(url) as response:
                data_zip = response.read()
        except urllib.error.URLError as e:
            print(f"Error downloading data: {e}")
            return None

        try:
            with zipfile.ZipFile(io.BytesIO(data_zip)) as zip_ref:
                data_file = zip_ref.namelist()[0]
                # Skip rows until the first actual date (row 6), and set the correct header.
                factors = pd.read_csv(zip_ref.open(data_file), skiprows=3, header=0)
        except zipfile.BadZipFile as e:
            print(f"Error opening zip file: {e}")
            return None
        factors.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        factors.index.names = ['Date']
        factors['Date'] = pd.to_datetime(factors['Date'], format='%Y%m%d')
        factors.set_index('Date', inplace=True)
        factors = factors.apply(pd.to_numeric, errors='coerce')
        factors = factors/100
        print(factors)
        return factors.tail(60) #return last 60 days of data