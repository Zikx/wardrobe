import os
import random
from datetime import date
import requests
import cv2
import decimal

from gtts import gTTS

# GET http://thecolorapi.com/id?hex=0047AB&rgb=0,71,171&hsl=215,100%,34%&cmyk=100,58,0,33&format=html
URL = 'http://thecolorapi.com/id'
filename = 'test.txt'

while(1):
    file = open(filename, 'r', encoding="utf8")
    text_rgb = file.read()
    file.close()

    split_data = text_rgb.split(',')
    if len(split_data) >= 4 and split_data[3].isdigit() == 1 and decimal.Decimal(split_data[3]) == 1:
        if split_data[0].isdigit() == 1 and split_data[1].isdigit() == 1 and split_data[2].isdigit() == 1 :
            print('raw data', text_rgb)
            rgb = list(map(int, split_data[0:3]))
            text_rgb = ','.join(map(str, (rgb[0:3])))
            if (rgb[0] >= 0 and rgb[0] <= 255 and
                rgb[1] >= 0 and rgb[0] <= 255 and
                rgb[2] >= 0 and rgb[0] <= 255):
                send_data = {'rgb' : text_rgb, 'format' : 'json'}
                res = requests.get(URL, params=send_data)
                test_json = res.json()
                color_text = test_json['name']['value']
                print(color_text)

                tts = gTTS(text=color_text, lang='en')
                t = date.today()
                m_mpfile = ("tts-%s-%s-%d-%d-%d.mp3" % (t, color_text, rgb[0], rgb[1], rgb[2]))
                tts.save(m_mpfile)
                os.system("start %s" % m_mpfile)

                file = open('test.txt', 'w', encoding='utf8')
                file.write('0,0,0,0,\n')
                file.close()
            else :
                print('wrong data')
        else :
            print('wrong data')


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
