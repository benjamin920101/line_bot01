import subprocess
import json
import os
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage

line_bot_api = LineBotApi('yIKuZJJWIk8yH9Bwwe2/U2X6h7FOBkbBBaA/IxZ1eVml+k7U8MVvNNUuS4xMHctvzkXdAIxeqQr8cAoWt7Kaf0XD3nBLBcVCsywAac1GcCewLA98XkVGbbpwsVcm5yzX2p6eVjxsKUPjftINBc5JvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cacecd1552c1f6e5eb64474596f4fec5')
# 导入revChatGPT.V1中的Chatbot类
from revChatGPT.V1 import Chatbot
# 创建Chatbot实例并传入config参数，包括登录OpenAI的账户信息
chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJiZW5qYW1pbjkyMDEwMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci01d3RWVnd0b2pMS0xLdFI4QUI0cWZTOGsifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6ImF1dGgwfDYzOThhMmFmNDIzMjIyOTJlZTZkZjYxOSIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODk5OTQzNzYsImV4cCI6MTY5MTIwMzk3NiwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.ju23l9KoSiN-G8sF6hXjqg-_NvxOgOBO1iNRBY9i3RFjhiJdV4eA5kJpSQod-otcTrYwmW10adBbDjuvI_kaqjTWpcyppMR7foX5W6oD1IsAFSdxrm4chwug2aCOvAa9e63PvKpLEZN_NZXTmbNbyEE9PjNb_EvpxzeM9CgP6dcD7A8buW7vTe7U9oZoewKKU9-ACHTA3paoyukWD-IZpKE6ugMYccALCeWPAYXUzHgtBGEJxD0IZV-lWxF4ICXn3EFIQHb69QYWwYa837nMXdG3D9K3al5rPqJxf4lFJmk-JHZ-yATi32_6kksf0jaNCQE4Et_vlTBLN_fmjTYlBQ",
  }) 
global person
person= "藥學系教授(Professor of Pharmacy)"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print(event.message.text)
    if event.message.text.startswith('/run '):
        command = event.message.text[5:]
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            message = TextSendMessage(text=output.decode('utf-8'))
        except subprocess.CalledProcessError as error:
            message = TextSendMessage(text=f"Command '{command}' failed with error code {error.returncode}:\n{error.output.decode('utf-8')}")
    elif event.message.text.startswith('/test'):
        # 定义prev_text变量，用于保存上一次对话的文本内容
        prev_text = ""
        q_dict = ["", "", "", "", "", "", "", "", "", ""]
        question = "prompt:我是心理師，直接智能功能狀態測驗（Mental Status Examination）（困難版）（繁體中文）（9題）(包含覺察力、處理速度、記憶力、抽象思考、語言等等）(題號用數字，不要題目1：，要1.)，生成"
        # 通过ask方法向ChatGPT发送问题并获取回答

        for data in chatbot.ask(question):            # 从回答数据中提取ChatGPT的回答，并去除前面已经输出过的文本部分
            message = data["message"][len(prev_text) :]
            # 输出ChatGPT的回答
            print(message, end="", flush=True)
            # 更新prev_text变量
            prev_text = data["message"]
        # 输出空行，以便下一轮对话
        print()
        #將題目分開
        for m in range(9):
            for i in range(len(prev_text)):
                if prev_text[i] == str(m+1) and prev_text[i+1] == ".":
                    for j in range(len(prev_text)):
                        if prev_text[j] == str(m+2) and prev_text[j+1] == ".":
                            q_dict[m] = prev_text[i+2:j-1]
                            q_dict[m] = str(m+1)+"."+q_dict[m]
                            print(q_dict[m])
                            q_dict[9] = q_dict[9] + q_dict[m] + "\n"
        prev_text = q_dict[9]
        message = TextSendMessage(text=prev_text)
    elif event.message.text.startswith('/ans '):
        # 定义prev_text变量，用于保存上一次对话的文本内容
        prev_text = ""
        question = q_dict[9] + event.message.text[5:]
        # 通过ask方法向ChatGPT发送问题并获取回答
        for data in chatbot.ask(question):            # 从回答数据中提取ChatGPT的回答，并去除前面已经输出过的文本部分
            message = data["message"][len(prev_text) :]
            # 输出ChatGPT的回答
            print(message, end="", flush=True)
            # 更新prev_text变量
            prev_text = data["message"]
        # 输出空行，以便下一轮对话
        print()
        message = TextSendMessage(text=prev_text)

    elif event.message.text.startswith('/set '):
        global person
        person = event.message.text[5:]
        print()
        message = TextSendMessage(text="set " + person + ",OK")

    elif event.message.text.startswith('/openai '):
        # 定义prev_text变量，用于保存上一次对话的文本内容
        prev_text = ""
        print(person)
        question = "prompt:你是Macy,是這裡的" + person + "。" + event.message.text[8:]
        # 通过ask方法向ChatGPT发送问题并获取回答
        for data in chatbot.ask(question):            # 从回答数据中提取ChatGPT的回答，并去除前面已经输出过的文本部分
            message = data["message"][len(prev_text) :]
            # 输出ChatGPT的回答
            print(message, end="", flush=True)
            # 更新prev_text变量
            prev_text = data["message"]
        # 输出空行，以便下一轮对话
        print()
        message = TextSendMessage(text=prev_text)
    else:
# 定义prev_text变量，用于保存上一次对话的文本内容
        prev_text = ""
        question = "prompt:你是Macy,是這裡的藥師(Pharmacist)。" + event.message.text[0:]
        # 通过ask方法向ChatGPT发送问题并获取回答
        for data in chatbot.ask(question):            # 从回答数据中提取ChatGPT的回答，并去除前面已经输出过的文本部分
            message = data["message"][len(prev_text) :]
            # 输出ChatGPT的回答
            print(message, end="", flush=True)
            # 更新prev_text变量
            prev_text = data["message"]
        # 输出空行，以便下一轮对话
        print()
        message = TextSendMessage(text=prev_text)

        # message = TextSendMessage(text='I did not understand your message.\n You can type /run <command> to run a command on the server.\n You can type /openai <question> to ask a question to the OpenAI GPT-3 API.')
    
    if event.message.text == 'test':
        message = TextSendMessage(text='OK')

    print(message)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(f"{event.message.id}.jpg", "wb") as file:
        for chunk in message_content.iter_content():
            file.write(chunk)
    message = TextSendMessage(text='Image received and saved.')
    print('Image received and saved.')
    line_bot_api.reply_message(event.reply_token, message)

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
    return HttpResponse(status=404)
