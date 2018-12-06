from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('1HXRWot+ttjTRNlW5WFaE0Znq6+qQD4uGIYtsFIUZjzKeEbZtxxkSZ3SsQ/uypy2NuqOTEhKa0waxFQcqhR5I3j152iOs4P5U0+/WgDzMKKy4YaRrFYSXkV9EEvkkeDxZy9CNgKVjpACKRNGTMv3BAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('85587d3f0d7c1bfdaa8402fba6f69db6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def KeyWord(text):
    KeyWordDict = {"你好":"你也好啊",
                   "你是誰":"我是大帥哥",
                   "帥":"帥炸了"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return[True,KeyWordDict[k]]
    return[False]

def Reply(event):

    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text))

def Button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='http://pic.uzzf.com/up/2017-4/2017419150548912.png',
            title='Menu',
            text='Please select',
            actions=[
                PostbackTemplateAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='message',
                    text='message text'
                ),
                URITemplateAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Button(event)
        #Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = str(e)))
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
