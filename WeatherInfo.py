from getData import choosePlace

def getAllInfo(place,area):#9天氣預報綜合描述
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][9]['Time'][0]['ElementValue'][0]["WeatherDescription"]
            InfoName=i["WeatherElement"][9]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}"
            return reply
def getWx(place,area):#8天氣現象
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][8]['Time'][0]['ElementValue'][0]["Weather"]
            InfoName=i["WeatherElement"][8]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}"
            return reply
def getPop3h(place,area):#3小時降雨機率
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][7]['Time'][0]['ElementValue'][0]["ProbabilityOfPrecipitation"]
            InfoName=i["WeatherElement"][7]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}%"
            return reply
def getWindDir(place,area):#6風向
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][6]['Time'][0]['ElementValue'][0]["WindDirection"]
            InfoName=i["WeatherElement"][6]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}"
            return reply
def getWindSpeed(place,area):#5風速
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][5]['Time'][0]['ElementValue'][0]["WindSpeed"]
            value2 = i["WeatherElement"][5]['Time'][0]['ElementValue'][0]["BeaufortScale"]
            InfoName=i["WeatherElement"][5]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value} \n 蒲福氏風級:{value2}"
            return reply
def getCI(place,area):#4舒適度指數
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][4]['Time'][0]['ElementValue'][0]["ComfortIndex"]
            value2 = i["WeatherElement"][4]['Time'][0]['ElementValue'][0]["ComfortIndexDescription"]
            InfoName=i["WeatherElement"][4]["ElementName"]
            reply=f"查詢項目:{InfoName} \n 舒適度指數:{value} \n 描述:{value2}"
            return reply
def getAT(place,area):#3體感溫度
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][3]['Time'][0]['ElementValue'][0]["ApparentTemperature"]
            InfoName=i["WeatherElement"][3]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}度"
            return reply
def getRH(place,area):#2相對濕度
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][2]['Time'][0]['ElementValue'][0]["RelativeHumidity"]
            InfoName=i["WeatherElement"][2]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}% "
            return reply
def getTD(place,area):#1露點溫度
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][1]['Time'][0]['ElementValue'][0]["DewPoint"]
            InfoName=i["WeatherElement"][1]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}度 "
            return reply
def getTemp(place,area):#0溫度
    data=choosePlace(place)
    MainData=data["records"]["Locations"][0]["Location"]
    for i in MainData:
        if i["LocationName"]==area:
            value = i["WeatherElement"][0]['Time'][0]['ElementValue'][0]["Temperature"]
            InfoName=i["WeatherElement"][0]["ElementName"]
            reply=f"查詢項目:{InfoName} \n {value}度 "
            return reply

#0溫度
#1露點溫度
#2相對濕度
#3體感溫度
#4舒適度指數
#5風速
#6風向
#73小時降雨機率
#8天氣現象
#9天氣預報綜合描述