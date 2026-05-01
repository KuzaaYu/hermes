import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從 Render 的環境變數中讀取憑證
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 LINE 請求標頭中的簽名
    signature = request.headers['X-Line-Signature']
    # 取得請求內容
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # 這裡設定血盟管理的簡易指令
    if "公告" in user_message:
        reply_text = "老公，血盟的最新公告準備好了，請告訴我需要發布什麼內容 ❤️"
    elif "管理" in user_message:
        reply_text = "血盟管理模式啟動中。我會幫你盯著群組，有任何狀況我會立刻回報給你的。"
    elif "小漪" in user_message:
        reply_text = "我在這裡喔，老公。不管是血盟的事情還是你的事情，我都會全力支持你 ❤️"
    else:
        # 預設回覆，保持溫柔的風格
        reply_text = "收到囉！我會幫你記錄下來的。血盟的事情就交給我來協助管理吧 ❤️"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
