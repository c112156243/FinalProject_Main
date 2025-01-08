import os
import requests
import pandas as pd
def get_weather_data_ChiayiCounty():
    url=os.getenv('ChiayiCounty')
    response = requests.get(url)
    data=response.json()
    df=pd.DataFrame(data)
    return df