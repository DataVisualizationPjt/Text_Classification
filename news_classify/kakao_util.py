#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import random as rd
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_code():
    driver = webdriver.Chrome()
    driver.get('https://kauth.kakao.com/oauth/authorize?client_id=5d0604180bf7d04d3e534b2fd8a0f37d&redirect_uri=https://ssk.com/oauth&response_type=code&scope=account_email')

    user_id = 'kimnh097@naver.com'
    user_passwd = '98520rla'

    driver.find_element(By.CSS_SELECTOR,r'#loginKey--1').send_keys(user_id)
    time.sleep(rd.uniform(0.3,1))

    driver.find_element(By.CSS_SELECTOR,r'#password--2').send_keys(user_passwd)
    time.sleep(rd.uniform(0.3,1))

    driver.find_element(By.CSS_SELECTOR,r'#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit').click()
    time.sleep(rd.uniform(2,2.5))


    code = (str(driver.current_url).split('code='))[-1]

    driver.quit()

    return code

def designate_to(code, to='friend'):
    if to=='friend':
        url = 'https://kauth.kakao.com/oauth/token'
        client_id = '5d0604180bf7d04d3e534b2fd8a0f37d'
        redirect_uri = 'https://ssk.com/oauth'

        data = {
            'grant_type' : 'authorization_code',
            'client_id' : client_id,
            'redirect_uri' : redirect_uri,
            'code' : code
            }

        response = requests.post(url, data=data)
        tokens = response.json()
        with open("token.json","r") as fp:
            tokens = json.load(fp)

        friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

        headers={"Authorization" : "Bearer " + tokens["access_token"]}

        result = json.loads(requests.get(friend_url, headers=headers).text)

        print(type(result))
        print("=============================================")
        print(result)
        print("=============================================")
        friends_list = result.get("elements")
        print(friends_list)
        # print(type(friends_list))
        print("=============================================")
        print(friends_list[0].get("uuid"))
        friend_id = friends_list[0].get("uuid")
        print(friend_id)

        friends_list = result.get("elements")
        friend_id = friends_list[0].get("uuid")
        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

        return send_url, headers

    if to=='me':

        data = {
            'grant_type' : 'authorization_code',
            'client_id' : client_id,
            'redirect_uri' : redirect_uri,
            'code' : code,
            'scope' : {'talk_message',
                    'profile_nickname',
                      'profile_image'
                      }
        }
        response = requests.post(url, data=data)
        tokens = response.json()

        with open("token.json", "r") as fp:
            tokens = json.load(fp)

        send_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {
            "Authorization": "Bearer " + tokens["access_token"]
        }

        return send_url, headers

