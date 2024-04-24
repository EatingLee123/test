# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/10 14:04
@Auth ： Eating Lee
@File ：loginTest.py
@IDE ：PyCharm

"""

import requests
import json
import time

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from getEncryptedPassword import get_encrypted_password


cloud_api = 'https://purangcloud-api.purang.com'
referer = 'https://pch5-front.purang.com/'
client_id = 'ATMzA4a2xx'
client_num = '2tGjeTRD7w3RMf5i2Pci'
idx = '0'
plain_text = '8023loveASD'
timeStamp = str(int(time.time()))[:10]

passwd = get_encrypted_password(cloud_api, client_id, client_num, timeStamp, idx, plain_text)

# 请求的URL
url = cloud_api + '/cloud/sys/auth/login'

# 请求的数据
data = {
    "loginType": "0",
    "name": "2106827098",
    "passwd": passwd,
    "phone": "",
    "smsCode": "",
    "clientId": client_id,
    "saveFlg": "N",
    "timeStamp": timeStamp
}

# 设置请求头部

headers = {
    'Content-Type': 'application/json',
    'Referer': referer,
    'from-source': 'PC'
}

# 发送POST请求
response = requests.post(url, json=data, headers=headers)

# 获取响应数据
response_data = response.json()

# 处理响应数据
if response.status_code == 200:
    # 请求成功，对响应数据进行处理
    print(response_data)
else:
    # 请求失败，打印错误信息
    print(f"请求失败，错误代码: {response.status_code}, 错误消息: {response_data.get('message')}")
