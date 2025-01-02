import os
import requests
from dotenv import load_dotenv
import pandas as pd
def get_weather_data_YilanCounty():
    url=os.getenv('YilanCounty')
    response = requests.get(url)
    data=response.json()
    df=pd.DataFrame(data)
    return df