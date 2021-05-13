
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
import requests
# import pyjwt as jwt
WECHAT_TOKEN = "yunze123"
# 微信APPID和secret
WECHAT_APPID = 'wx0608d425f1efc89d'
WECHAT_SECRET = 'b18839a2ea1d80674ebb2ac354d79bc6'


def get_access_token(code):
    """
    :param code:前端截取微信平台发送的code
    :return: openid和access_token
    """
    payload = {'appid': WECHAT_APPID, 'secret': WECHAT_SECRET, 'code': code, 'grant_type': 'authorization_code'}
    access_token_get = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params=payload)
    access_token_get_json = access_token_get.json()
    openid = access_token_get_json["openid"]
    access_token = access_token_get_json["access_token"]
    return openid, access_token


def en_token(value):
    """
    :param value:需要jwt加密的信息
    :return: 加密后的token值
    """
    in_token = jwt.encode({"id": value}, 'yunze', algorithm='HS256')
    return in_token


def de_token(token):
    """
    :param token:jwt token的值
    :return: jwt解密后的值
    """
    token_value = eval(token)
    out_token = jwt.decode(token_value, 'yunze', algorithms=['HS256'])
    return out_token

