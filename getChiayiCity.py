import os
import requests
import pandas as pd
def get_weather_data_ChiayiCity():
    url=os.getenv('ChiayiCity')
    response = requests.get(url)
    data=response.json()
    df=pd.DataFrame(data)
    return df
