from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

import string
import random
import cv2 as cv
import subprocess
import os
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message = []

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if event.message.type=='text':
                    mtext=event.message.text
                    message.append(TextSendMessage(text=mtext))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='image':
                    image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                    image_content = line_bot_api.get_message_content(event.message.id)
                    image_name = image_name.upper()+'.jpg'
                    path='C:\\dfdc\\code\\iot\\static\\image\\' + image_name
                    with open(path, 'wb') as fd:
                        for chunk in image_content.iter_content():
                            fd.write(chunk)
                   
                    # img = cv.imread(path)
                    # sp = img.shape
                    # height = str(sp[0])
                    # width = str(sp[1])
                    # size = width + ' * ' + height
                    # message.append(TextSendMessage(text='圖片名稱：'+ image_name + '\n' + '圖片尺寸：' + size))
                    output = subprocess.check_output(["python", "C:\\dfdc\\code\\deepface_detect_image.py", path])
                    output = output.decode('BIG5')
                    print(output.split('$')[1])
                    message.append(TextSendMessage(output.split('$')[1]))
                    line_bot_api.reply_message(event.reply_token,message)
                    os.remove(path)
                    
                elif event.message.type=='video':
                    video_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                    video_content = line_bot_api.get_message_content(event.message.id)
                    video_name = video_name.upper()+'.mp4'
                    path='C:\\dfdc\\code\\iot\\static\\video\\' + video_name #要改路徑
                    with open(path, 'wb') as fd:
                        for chunk in video_content.iter_content():
                            fd.write(chunk)
                    # cap = cv.VideoCapture(path)
                    # fps = cap.get(cv.CAP_PROP_FPS)
                    # frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
                    # duration = frame_count/fps
                    # height = str(int(cap.get(4)))
                    # width = str(int(cap.get(3)))
                    # size = width + ' * ' + height
                    output = subprocess.check_output(["python", "C:\\dfdc\\code\\deepface_detect_video.py", path])
                    output = output.decode('BIG5')
                    print(output.split('$')[1])
                    message.append(TextSendMessage(output.split('$')[1]))
                    line_bot_api.reply_message(event.reply_token,message)
                    os.remove(path)
                    # cap.release()

                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='偷傳語音欸$',
                        emojis=[
                            {
                                'index': 5, 
                                'productId': '5ac21c46040ab15980c9b442', 
                                'emojiId': '008'
                            },
                    ],))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='file':
                    message.append(TextSendMessage(text='不要傳怪檔案欸$',
                        emojis=[
                            {
                                'index': 7, 
                                'productId': '5ac21c46040ab15980c9b442', 
                                'emojiId': '003'
                            },
                    ],))
                    line_bot_api.reply_message(event.reply_token,message)
                
                elif event.message.type=='location':
                    message.append(TextSendMessage(text='偷偷跟蹤你嘿嘿$',
                        emojis=[
                            {
                                'index': 7, 
                                'productId': '5ac1bfd5040ab15980c9b435', 
                                'emojiId': '008'
                            },
                    ],))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='sticker':
                    message.append(TextSendMessage(text='偷傳貼圖齁哈哈哈哈！！！'))
                    message.append(StickerSendMessage(
                        package_id='8525',  
                        sticker_id='16581296'
                    ))
                    line_bot_api.reply_message(event.reply_token, message)
                    
        return HttpResponse()
    else:
        return HttpResponseBadRequest()