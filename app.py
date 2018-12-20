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

#會員系統
def GetUserlist():
    userlist = {}
    file = open('users','r')
    while True :
        temp = file.readline().strip().split(',')
        if temp[0] == "" : break
        userlist[temp[0]] = temp[1]
    file.close()
    return userlist

#登入系統
def Login(event,userlist):
    i = 0
    for user in userlist.keys():
        if event.source.user_id == user:
            return i
        i+=1
    return -1

#寫入資料
def Update(userlist):
    file = open('users','w')
    for user in userlist.keys():
        file.write(user+','+userlist[user])
    file.close()

#關鍵字系統
def KeyWord(event):
    KeyWordDict = {"你好":"你也好啊",
                   "你是誰":"我是大帥哥",
                   "帥":"帥炸了",
                   "差不多了":"讚!!!"}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

#按鈕版面系統
def Button(event):
    return TemplateSendMessage(
        alt_text='特殊訊息，請進入手機查看',
        template=ButtonsTemplate(
            thumbnail_image_url='https://github.com/54bp6cl6/LineBotClass/blob/master/logo.jpg?raw=true',
            title='HPClub - Line Bot 教學',
            text='大家學會了ㄇ',
            actions=[
                PostbackTemplateAction(
                    label='還沒',
                    data='還沒'
                ),
                MessageTemplateAction(
                    label='差不多了',
                    text='差不多了'
                ),
                URITemplateAction(
                    label='幫我們按個讚',
                    uri='https://www.facebook.com/ShuHPclub'
                )
            ]
        )
    )

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U95418ebc4fffefdd89088d6f9dabd75b":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False

#新增一個參數
def Reply(event,userlist):
    if not Command(event):
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = Ktemp[1]))
        else:
            if userlist[event.source.user_id] == '-1':
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎？"))
                userlist[event.source.user_id] = '0'
            else:
                if event.message.text == "黑面琵鷺":
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "你居然知道答案!!!"))
                else:
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
                userlist[event.source.user_id] = '-1'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userlist = GetUserlist()
        clientindex = Login(event,userlist)
        if clientindex > -1:
            Reply(event,userlist)
            '''
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.source.user_id + "說:"))
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.message.text))
            '''
        else:
            userlist[event.source.user_id] = '-1';
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="註冊成功"))
        Update(userlist)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "還沒":
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text="還沒就趕快練習去~~~"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
