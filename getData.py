from getYilanCounty import get_weather_data_YilanCounty
from getTaoyuanCity import get_weather_data_TaoyuanCity
from getXinzhuCounty import get_weather_data_XinzhuCounty
from getMioliCounty import get_weather_data_MioliCounty
from getChanghuaCounty import get_weather_data_ChanghuaCounty
from getNantouCounty import get_weather_data_NantouCounty
from getYunlinCounty import get_weather_data_YunlinCounty
from getChiayiCounty import get_weather_data_ChiayiCounty
from getTaidongCounty import get_weather_data_TaidongCounty
from getHualienCounty import get_weather_data_HualienCounty
from getPingtungCounty import get_weather_data_PingtungCounty
from getPenghuCounty import get_weather_data_PenghuCounty
from getJilongCity import get_weather_data_JilongCity
from getXinzhuCity import get_weather_data_XinzhuCity
from getChiayiCity import get_weather_data_ChiayiCity
from getTaipeiCity import get_weather_data_TaipeiCity
from getKaohsiungCity import get_weather_data_KaohsiungCity
from getXinbeiCity import get_weather_data_XinbeiCity
from getTaizhongCity import get_weather_data_TaizhongCity
from getTainanCity import get_weather_data_TainanCity
from getLianjiangCounty import get_weather_data_LianjiangCounty
from getKinmenCounty import get_weather_data_KinmenCounty
def choosePlace(place):
    if place=="宜蘭縣":
        data=get_weather_data_YilanCounty()
    elif place=="桃園市":
        data=get_weather_data_TaoyuanCity()
    elif place=="新竹縣":
        data=get_weather_data_XinzhuCounty()
    elif place=="苗栗縣":
        data=get_weather_data_MioliCounty()
    elif place=="彰化縣":
        data=get_weather_data_ChanghuaCounty()
    elif place=="南投縣":
        data=get_weather_data_NantouCounty()
    elif place=="雲林縣":
        data=get_weather_data_YunlinCounty()
    elif place=="嘉義縣":
        data=get_weather_data_ChiayiCounty()
    elif place=="臺東縣":
        data=get_weather_data_TaidongCounty()
    elif place=="花蓮縣":
        data=get_weather_data_HualienCounty()
    elif place=="屏東縣":
        data=get_weather_data_PingtungCounty()
    elif place=="澎湖縣":
        data=get_weather_data_PenghuCounty()
    elif place=="基隆市":
        data=get_weather_data_JilongCity()
    elif place=="新竹市":
        data=get_weather_data_XinzhuCity()
    elif place=="嘉義市":
        data=get_weather_data_ChiayiCity()
    elif place=="臺北市":
        data=get_weather_data_TaipeiCity()
    elif place=="高雄市":
        data=get_weather_data_KaohsiungCity()
    elif place=="新北市":
        data=get_weather_data_XinbeiCity()
    elif place=="臺中市":
        data=get_weather_data_TaizhongCity()
    elif place=="臺南市":
        data=get_weather_data_TainanCity()
    elif place=="連江縣":
        data=get_weather_data_LianjiangCounty()
    elif place=="金門縣":
        data=get_weather_data_KinmenCounty()
    else:
        raise ValueError(f"未知的地點: {place}")
    return data