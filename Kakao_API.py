#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import requests
import json
import pandas as pd
from PyKakao import Message
from news_classify.prediction import prediction
from news_classify.kakao_util import *

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',"--to", dest='to', default='friend', action="store")
    opt = parser.parse_args()
    return opt

def send(to='friend'):
    code = get_code()
    designate_to(code,to=to)

    news_list = []
    df = prediction('./best.h5')
    df = (df.sort_values('interested', ascending = False))[:3]

    for i in df.index:
        title = df.loc[i, 'title']
        interest = df.loc[i, 'interested']
        link = df.loc[i, 'link']
        news_list.append((title, interest, link))

    message = '♨ 따끈한 최신 뉴스가 도착했어요 ♨\n\n'

    for idx, (title, interest, link) in enumerate(news_list, start=1):
        message += f'{idx}. {round((interest*100),2)}% 확률로 관심 뉴스에요!\n[{title}]\n{link}\n\n'
    
    if to=='friend':
        data = {
            'receiver_uuids': '["{}"]'.format(friend_id),
            'template_object' : json.dumps
            ({'object_type': 'text',
                    'text': message,
                    'link': {
                        'web_url': 'https://developers.kakao.com',
                        'mobile_web_url': 'https://developers.kakao.com'
                    },
                    'button_title': '바로 확인'})
            }
    if to=='me':
        data = {
            'template_object' : json.dumps
            ({'object_type': 'text',
                    'text': message,
                    'link': {
                        'web_url': 'https://developers.kakao.com',
                        'mobile_web_url': 'https://developers.kakao.com'
                    },
                    'button_title': '바로 확인'})

    response_status_list = []

    data_json = {'template_object': json.dumps(data)}
    response = requests.post(send_url, headers=headers, data=data)
    response_status = response.status_code
    response_status_list.append(response_status)

    print(response_status)
    print(response_status_list)

    response.status_code
    
def main(opt):
    send(opt)
    
if __name__ == '__main__':
    opt = parse_opt()
    main(opt.to)

