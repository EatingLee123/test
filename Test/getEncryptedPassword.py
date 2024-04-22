# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/17 20:45
@Auth ： Eating Lee
@File ：getEncryptedPassword.py
@IDE ：PyCharm

"""
import requests
import json
import time
import hashlib

import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

#AES解密
def aes_decrypt(encrypt_str, key):
    """
    使用AES解密算法对密文进行解密

    参数：
    encrypt_str (str): 要解密的密文
    key (str): 密钥

    返回：
    str: 解密后的明文
    """
    try:
        aes_key = key.encode('utf-8')
        cipher = AES.new(aes_key, AES.MODE_ECB)
        decrypted_bytes = cipher.decrypt(base64.b64decode(encrypt_str))
        decrypt_content = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
        print(f"解密后: {decrypt_content}")
        return decrypt_content
    except Exception as e:
        print(f"解密异常: {e}")
        return None

#AES加密
def aes_encrypt(content, key):
    """
    使用AES加密算法对明文进行加密

    参数：
    content (str): 要加密的明文
    key (str): 密钥

    返回：
    str: 加密后的密文
    """
    try:
        aes_key = key.encode('utf-8')
        content=md5_hash = hashlib.md5(content.encode()).hexdigest()
        cipher = AES.new(aes_key, AES.MODE_ECB)
        padded_content = pad(content.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_content)
        encrypt_str = base64.b64encode(encrypted_bytes).decode('utf-8')
        print(f"加密后: {encrypt_str}")
        return encrypt_str
    except Exception as e:
        print(f"加密异常: {e}")
        return None

#获取加密后的密码
def get_encrypted_password(cloud_api, client_id, client_num, timeStamp, idx, plain_text):
    """
    获取加密后的密码

    参数：
    cloud_api (str): 云服务API地址
    client_id (str): 客户端ID
    client_num (str): 客户端编号
    timeStamp (str): 时间戳
    idx (str): 索引
    plain_text (str): 需要加密的明文密码

    返回：
    str: 加密后的密码
    """
    # 定义请求的URL和报文数据
    url = cloud_api + '/cloud/sys/auth/skey'
    data = {
        'clientId': client_id,
        'timeStamp': timeStamp,
        'clientNum': client_num,
        'idx': idx
    }

    # 将字典类型的 data 转换为 JSON 字符串
    json_data = json.dumps(data)

    # 设置请求头部
    headers = {
        'Content-Type': 'application/json',
        'from-source': 'PC'
    }

    # 发送 POST 请求，获取响应
    response = requests.post(url, data=json_data, headers=headers)

    # 存储响应
    data = response.json()

    if response.status_code == 200 and data.get('success') == True:
        serverNum = data['data']['serverNum']
        flg = data['data']['flg']
        expireTime = data['data']['expireTime']

        idx = int(idx)
        cNumb = client_num[idx:idx + 16]
        serName = aes_decrypt(serverNum, cNumb)

        key = hashlib.md5((cNumb + serName).encode()).hexdigest()
        # print('key:',key)
        # print('flg:',flg)

        if flg == 0:
            key = key[:16]
        else:
            key = key[16:]

        # print('key:', key)

        passwdAes = aes_encrypt(plain_text, key)

        return passwdAes


# 示例用法
# cloud_api = 'https://purangcloud-api.purang.com'
# client_id = 'ATMzA4a2xx'
# client_num = '2tGjeTRD7w3RMf5i2Pci'
# idx = '0'
# plain_text = '123456'
# timeStamp = str(int(time.time()))
#
# encrypted_password = get_encrypted_password(cloud_api, client_id, client_num, timeStamp, idx, plain_text)