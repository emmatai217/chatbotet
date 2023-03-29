from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('lD1Rqr2R8Vh7CC0tgth6l0ruUqEZ8cvHVlLulaM2vS+Q50X42aKgCgnEaC8cd+hAFEG6edlAFomePJ/fdti1OBLQyf0eIVnhkFVuSOxfVCUBsf/euc162AJA/NkpN4SGD/6iPz0AFJxs/xQ5oBvozAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3541c02f308687b4a02c8d62dd5634bb')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
