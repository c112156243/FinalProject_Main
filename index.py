import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.v3.webhooks import FollowEvent
from linebot.v3.messaging import Configuration,MessagingApi,MessagingApiBlob,RichMenuSize,RichMenuArea,RichMenuRequest,RichMenuBounds,MessageAction,ApiClient
from dotenv import load_dotenv
load_dotenv()
from WeatherInfo import  getAllInfo, getTemp, getCI, getAT, getRH, getTD, getWindSpeed, getWindDir, getPop3h, getWx
import sys
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
                    width=826, 
                    height=831
                ),
                action=MessageAction(text="高雄市 燕巢區 溫度")
            ),   
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=831,    
                    y=0, 
                    width=834, 
                    height=826
                ),
                action=MessageAction(text="高雄市 燕巢區 舒適度指數")
            ),RichMenuArea(
                bounds=RichMenuBounds(
                    x=1661,    
                    y=0, 
                    width=835, 
                    height=831
                ),
                action=MessageAction(text="高雄市 燕巢區 體感溫度")
            ),RichMenuArea(
                bounds=RichMenuBounds(
                    x=0,    
                    y=839, 
                    width=826, 
                    height=835
                ),
                action=MessageAction(text="高雄市 燕巢區 相對濕度")
            ),RichMenuArea(
                bounds=RichMenuBounds(
                    x=831,    
                    y=843, 
                    width=830, 
                    height=835
                ),
                action=MessageAction(text="高雄市  燕巢區 露點溫度")
            ),RichMenuArea(
                bounds=RichMenuBounds(
                    x=1678,    
                    y=847, 
                    width=814, 
                    height=822
                ),
                action=MessageAction(text="高雄市 燕巢區 風速")
            ),
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

        with open("stastic/richmenu.png", "rb") as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={"Content-Type": "image/png"}
            )
        
        line_bot_api.set_default_rich_menu(rich_menu_id)
create_rich_menu1()

@handler.add(FollowEvent)
def handle_follow(event):
    print(f'Got{event.type} event')  #加入好友的事件

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text.split()
    reply = "輸入錯誤"
    if len(user_input) == 2:
        place, area = user_input
        if place.endswith('縣') or place.endswith('市'):
            if area.endswith('區') or area.endswith('市') or area.endswith('鄉') or area.endswith('鎮') or area.endswith('村')  or area.endswith('里') or area.endswith('鄰'):
                reply=getAllInfo(place,area)
            else:
                reply = "輸入錯誤"
        else:
            reply = "輸入錯誤"
    else:
        reply = "輸入錯誤"

    if len(user_input) == 3:
        place,area,attribute = user_input
        if attribute=='溫度':
            reply = getTemp(place,area)
        elif attribute=='舒適度指數':
            reply = getCI(place,area)
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
        elif attribute=='天氣現象':
            reply = getWx(place,area)
        else:
            reply = "輸入錯誤"
        
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()