import os
import requests
import pandas as pd
def get_weather_data_TaoyuanCity():
    url=os.getenv('TaoyuanCity')
    response = requests.get(url)
    data=response.json()
    df=pd.DataFrame(data)
    return df
