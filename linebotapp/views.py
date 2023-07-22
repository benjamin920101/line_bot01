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
    "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..XBElUqTY-juuAzbw.jhkbb7GsTGiLXeylUJsbhJSzEGzeR96myG0Bgl84eQWyts2S5x1OaLjjMy2q-QKr6L0CkrJAi_vMUhW71jbkuIsvAVG1ySnv1GH16QLtiARZvzqV3Sty-X3Us8lBz0Rm45VzzT10tP0TJ3mkG7tv2Lcy8XyxAqRq7wYMbANkk3S_BiJaP_kYzvmMP6PBfcGyKuhoMsf0FJrHul-UK4HHotv5O1Vur_RfLlG1UHG01hRtcfd5au6kBgpL7m9Jky74JTBpwP7waV7W6WBJnh7-BuxFexQhFviZgSp9OYHmZr_rlucNUWwkh6_7Zrp56kc___QW1e53o1nY9Z6_u0PgCWfzJjalQf7Jg1y4IDrccJMt6i2BQ4CvNNU-oOavBODo1HkIqNcrjKMndF-NVAkWZfRRazaqZYAIvNszkroDSEq94a7ZuRUQs_xqSnwTl4vcS5wRd69DuQa34MhrkdMRWkJ_brNJC9KJwJHhxDxCRI0J4oy9_e9J5pbVd7VUryxVsUSFvNoklVuO-y-dzegKk13dfrezqpoP2DcjL6rLB6x5I1F1xWZyJOzEe-WB-7ZneKiQZunrL4jLwRRIYlH2U0M2xd9vcXxKLQJqnFycqlr4z3RT-mj6swlFhP150ItUoDPF-YR_pwRCI6kg3mMum5NGoxp4IkgwfW2LEcRqsNJOpbRv_A2_yiGdLisf_TX4wEdQJaLGKgWO3TuwNxps92hY05rkbTO7O_6QWXoaL-7_O9CCFchEJgCe4ARHWDL3YWOi0c6kYGlgxvmyZBPuXKH70TskShmUeBMystyvpBJ2yN7rmga7J9_7AcFSVoAI5zufnWBSFEt72OxMZ_pH8p0t95TOLjtMUZJl1asPUyU1PFlJ2nMS6k_GfDEkvyE1c6XABspjKLBsO0abMPfoEkJd2b3b-f34SkQYBUCi21NY-DTUTCWm9LwUf8vldPKlrM2VXiay1kIn03Wd6-Stl7Zmwz8MWYE19m84IwRQcjnHpxny0lQiPtOuoLnUb915tOZNBEILh-LP0YOgSXLxZPGzuSTQ_D-zHk0eHPPd7PTaioAoAZxDJUtA6gymIp_HkyfIDslYuYfrxIVJbAnih2JK4Ebi8cJedCXhizhuyv2KAMyJCBV8dtzDMqJ7PDVTTkO36pScRHqYKIffAYoIXoXyOGabj0Y6rAtXvQ4n4k63USVnoIhYCCczer06prq0uF3xKlIvtDdoliWYXZShCdP32GwIvuV_67OGsKeDDqPnyFxRdyfJTW7Q3rbXr2xcuX9TWpGN3iOnW6pWmJ9fXTgmG1jpoxiIp6V6S4l_cp_85oj6ArQJSIhv0FfF-OsXLSl4SzLIG8C3k6jFZDPGxeBXheUu6l0lj2_Hk0nmBub_Zg6SNTGoSteGEPCYWnVb6JT--ACmOGd1SzvOmcFjViGrOH1vD0XLMeO5GuTUYmBBOYE6QOZOOlCQ6ZDeADSPGrWOBm90qnxdFr8CQc1hwcTsfD-yMrKdYfwHLol_I4ulHgkfbet1ALmH1QaPzUOwG2J6ZZIFZ-6I_Six6fiB1UWhcTP3--8Ewzf65RgSxiR60AxzNOPcfOnXJpbGqtaPbJSsfusUGnhKCdun7yuy6_GUiCJF68H3XHpU2aAHxV2jmvrAtwtMZh0VVlUKXUez074PtKbj0Ew_mwlIouzUmtQnWFwSrZP4OIejQyZqmMxzKmL0EosW2I879rX78sEw9Ez1VinHMlwsAo5R3BV8HaGnte4jILir1Zs3naKpD1TnTpw0PDIIjBlu393HvrsR9sat0nIh8rQvBiuj6t1PXkW7ffLP4sjoUmIrI0RMpdnMYFqWzY3YwfOSFHFN394YlSGzQSjeAJL8SwhkDij51yo9RQwzqzbDA7i26sjRxEL4rczmoaPEhnywIjLjzvLGUbpH69KpWrbvT53WwJHJfrZSesWydyGJyu2Dz3AHbXj5MfQ9Hx3Hmgdw9r9QmZJI4jq6RZLm1ctEYJe02GfUQmfsiWy8byYKaj1gQIh2banbTWkFSNObRVdTNF-aVEBWh5guM2lMp73IPwaGWF-y5t4tbQTUc9ZsGivzJRXJb0PGpFT1mZDgpOZ5BoAF77t4HlnH0MVhoTWCl037EGJtTXmtqsfLPfnxsGymC8J9BlRjzUvIfFCA3LC-j4oPxjg7qGIpe7xrG98Rt0aVFLqwFX8Ifl1KLkehlcesx8DZmIyNSnR95tS0bXCTxU_jZWi-EyBDtzvgE25Sg_vB4nNtNnRVgzugfczt8_UF_d6vQ12rZY4-MRxBx3RulZbtw8n2BAE5YdWs_CisNyFq4K44o8QA9kxIlBUAYTvGEAW2_vyT86Ftk6h0uGvIJplKWFfIRnBgEf6kXoa8o24HU4lJnFYZyx8cZc8lY8sBxvFcrGj3Q4ZeqSYQbEVduTq0qcJkatbU_-yhTBw2JB2zZPxIwVuYbE_AClHAtE2KDnHIEym67xZstz_UzypRqm04h83vF1_Z_bZcztVwunVBPbHlqz5eE9WOc6OGFMNZ5GugNEIYId4KR4A_G9SWGfWLYnxfbnCNmYmH-kR1njH1OSRZd0L5yUNBczDY2-d5552j3yfpd67zTW41rOWyKA_SYobuVj_aG_mgUC7b3166ptwiFJged0QxWiMdpM9ZJA6BgpyLKHD_jDHzjFwWvnufKz0BtpgJXiLVNnnpKT0OOigyD4i9sZiKYzoysKT9Pt7sC185InkMBDgKPS9WkFmo1OZBqHb6p6cwFKZfljgcERVaxBmc6h3eCuBxt7Bz8aJoGDA9DPFxdqS_9ed_gqYzJVFCcP4u684fy8PDcHM4Jo2E_wNWeyoxlZkHiQD1euEmPPU4GlySYEnpR-hJ7TdkebMGtVOK7g.kTJJ20BK4gEbvWnbLG8okg",
    "cf_clearance": "JkZZzi.zDhohdI9.xijsCRguNiJ1QqvVprtGFc_uQh8-1689992080-0-1-b97506f5.d660bc9e.66e22ef2-0.2.1689992080",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
  }) 


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
    elif event.message.text.startswith('/openai '):
        # 定义prev_text变量，用于保存上一次对话的文本内容
        prev_text = ""
        question = "prompt:你是Macy,是這裡的藥學系教授(Professor of Pharmacy)。" + event.message.text[8:]
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
        question = event.message.text[0:]
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
    elif event.message.text == 'no':
        message = TextSendMessage(text='yes')
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
