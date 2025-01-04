import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
load_dotenv()
from WeatherInfo import  getAllInfo, getTemp, getCI, getAT, getRH, getTD, getWindSpeed, getWindDir, getPop3h, getWx
import sys
print(sys.path)

app = Flask(__name__)

# LINE BOT API 設定
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

hahahaha = "hahahaha"

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