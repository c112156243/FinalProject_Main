import os
import requests
import pandas as pd
def get_weather_data_XinzhuCounty():
    url=os.getenv('XinzhuCounty')
    response = requests.get(url)
    data=response.json()
    df=pd.DataFrame(data)
    return df
