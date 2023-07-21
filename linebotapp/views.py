from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi('yIKuZJJWIk8yH9Bwwe2/U2X6h7FOBkbBBaA/IxZ1eVml+k7U8MVvNNUuS4xMHctvzkXdAIxeqQr8cAoWt7Kaf0XD3nBLBcVCsywAac1GcCewLA98XkVGbbpwsVcm5yzX2p6eVjxsKUPjftINBc5JvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cacecd1552c1f6e5eb64474596f4fec5')

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print(event.message.text)
    if event.message.text == 'hi':
        message = TextSendMessage(text='hello')
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text == 'no':
        message = TextSendMessage(text='yes')
        line_bot_api.reply_message(event.reply_token, message)