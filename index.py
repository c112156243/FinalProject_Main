import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
from linebot.v3.webhooks import FollowEvent
from linebot.v3.messaging import Configuration,MessagingApi,MessagingApiBlob,RichMenuSize,RichMenuArea,RichMenuRequest,RichMenuBounds,MessageAction,ApiClient
from WeatherInfo import  getAllInfo, getTemp, getCI, getAT, getRH, getTD, getWindSpeed, getWindDir, getPop3h, getWx
import sys
import time
import json
print(sys.path)

app = Flask(__name__)

# LINE BOT API 設定
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
configuration =Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))



@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def create_rich_menu1():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)
    
        areas =[
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=0,    
                    y=0, 
                    width=1223, 
                    height=1677
                ),
                action=MessageAction(text="!天氣查詢")
            ),   
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=1200,    
                    y=0, 
                    width=1280, 
                    height=843
                ),
                action=MessageAction(text="!雷達回波圖")
            ),RichMenuArea(
                bounds=RichMenuBounds(
                    x=1220,    
                    y=838, 
                    width=1280, 
                    height=843
                ),
                action=MessageAction(text="!地震")
            )
        ]

        rich_menu_to_create = RichMenuRequest(
            size=RichMenuSize(
                width=2500, 
                height=1686
            ),
            selected=True,
            name="圖文選單1",
            chatBarText="收起選單",
            areas=areas
        )

        rich_menu_id=line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_create
        ).rich_menu_id

        with open("static/richmenu.png", "rb") as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={"Content-Type": "image/png"}
            )
        
        line_bot_api.set_default_rich_menu(rich_menu_id)
create_rich_menu1()

def earth_quake():
    result = []
    try:
        code = 'CWA-72AC6F5C-B8DC-4FF7-A1A5-A220898EDF10'
        # 小區域 https://opendata.cwa.gov.tw/dataset/earthquake/E-A0016-001
        url = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={code}'
        req1 = requests.get(url)  # 爬取資料
        data1 = req1.json()       # 轉換成 json
        eq1 = data1['records']['Earthquake'][0]           # 取得第一筆地震資訊
        t1 = data1['records']['Earthquake'][0]['EarthquakeInfo']['OriginTime']
        # 顯著有感 https://opendata.cwa.gov.tw/dataset/all/E-A0015-001
        url2 = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={code}'
        req2 = requests.get(url2)  # 爬取資料
        data2 = req2.json()        # 轉換成 json
        eq2 = data2['records']['Earthquake'][0]           # 取得第一筆地震資訊
        t2 = data2['records']['Earthquake'][0]['EarthquakeInfo']['OriginTime']
        
        result = [eq1['ReportContent'], eq1['ReportImageURI']] # 先使用小區域地震
        if t2>t1:
          result = [eq2['ReportContent'], eq2['ReportImageURI']] # 如果顯著有感地震時間較近，就用顯著有感地震
    except Exception as e:
        print(e)
        result = ['抓取失敗...','']
    return result
earth_quake()

def weather(address):
    result = {}
    code = 'CWA-72AC6F5C-B8DC-4FF7-A1A5-A220898EDF10'
    # 即時天氣
    try:
        url = [f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={code}',
            f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization={code}']
        for item in url:
            req = requests.get(item)   # 爬取目前天氣網址的資料
            data = req.json()
            station = data['records']['Station']
            for i in station:
                city = i['GeoInfo']['CountyName']
                area = i['GeoInfo']['TownName']
                if not f'{city}{area}' in result:
                    weather = i['WeatherElement']['Weather']
                    temp = i['WeatherElement']['AirTemperature']
                    humid = i['WeatherElement']['RelativeHumidity']
                    result[f'{city}{area}'] = f'目前天氣狀況「{weather}」，溫度 {temp} 度，相對濕度 {humid}%！'
    except:
        pass

@handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got{event.type} event')  #加入好友的事件

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_token = event.reply_token
    user_id = event.source.user_id
    
    if text == '!天氣查詢':
        line_bot_api.reply_message(reply_token, TextSendMessage(text='請輸入縣市名稱及區域名稱，例如：高雄市 燕巢區 或 高雄市 燕巢區 溫度來獲取更多資訊!'))
    elif text == '!雷達回波圖' or text == '!雷達回波':
        line_bot_api.push_message(user_id, TextSendMessage(text='別再催了！竊取資料中，等一下....'))
        img_url = f'https://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-A0058-001.png?{time.time_ns()}'
        img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
        line_bot_api.reply_message(reply_token, img_message)
    elif text == '!地震':
                line_bot_api.push_message(user_id, TextSendMessage(text='我翻一下抽屜....請問你在急甚麼?'))
                reply = earth_quake()   # 執行函式，讀取數值
                text_message = TextSendMessage(text=reply[0])        # 取得文字內容
                line_bot_api.reply_message(reply_token,text_message) # 傳送文字
                line_bot_api.push_message(user_id, ImageSendMessage(original_content_url=reply[1], preview_image_url=reply[1])) # 傳送圖片
    else:
        user_input = text.split()
        reply = "輸入錯誤"
        if len(user_input) == 2:
            place, area = user_input
            if place.endswith('縣') or place.endswith('市'):
                if area.endswith('區') or area.endswith('市') or area.endswith('鄉') or area.endswith('鎮') or area.endswith('村') or area.endswith('里') or area.endswith('鄰'):
                    reply = getAllInfo(place, area)
                else:
                    reply = "輸入錯誤"
            else:
                reply = "輸入錯誤"
        elif len(user_input) == 3:
            place, area, attribute = user_input
            if attribute == '溫度':
                reply = getTemp(place, area)
            elif attribute == '舒適度指數':
                reply = getCI(place, area)
            elif attribute=='體感溫度':
                reply = getAT(place,area)
            elif attribute=='相對濕度':
                reply = getRH(place,area)
            elif attribute=='露點溫度':
                reply = getTD(place,area)
            elif attribute=='風速':
                reply = getWindSpeed(place,area)
            elif attribute=='風向':
                reply = getWindDir(place,area)
            elif attribute=='降雨機率':
                reply = getPop3h(place,area)
            elif attribute=='天氣現象'  :
                reply = getWx(place,area)
            else:
                reply = "輸入錯誤"
        else:
            reply = "輸入錯誤"
        
        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()
