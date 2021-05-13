#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
"""
注册接口
"""
from flask import Blueprint, request, redirect, session
from urllib import parse
from utils.users.wechat import en_token, de_token, get_access_token
import json
from flask_jwt_extended import jwt_required, get_jwt_identity
register = Blueprint('register_bp', __name__)
WECHAT_TOKEN = "yunze123"
WECHAT_APPID = 'wx0608d425f1efc89d'
WECHAT_SECRET = 'b18839a2ea1d80674ebb2ac354d79bc6'


# 微信认证请求接口
@register.route('/get_wxauth', methods=['GET'])
def get_wxauth():
    hostname = "http://127.0.0.1:5000"
    en_url = parse.quote(hostname + "/wechat_login")
    authorize_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&" \
                   "scope=snsapi_userinfo&state=STATE#wechat_redirect".format(WECHAT_APPID, en_url)
    wxauth = {"status": 200, "url": authorize_url}
    json_wxauth = json.dumps(wxauth, sort_keys=True, indent=4)
    return json_wxauth, 200


@register.route('/wechat_login', methods=['GET'])
def wechat_login():
    # 获取前端微信的code
    code = request.args.get("code")
    openid, access_token = get_access_token(code)
    token = en_token(openid)
    msg = 200
    redirect_url = 'http://127.0.0.1:8080/author?token={0}&msg={1}'.format(token, msg)
    return redirect(redirect_url)


# 获取个人信息接口
@register.route('/get_user_info', methods=['POST'])
def get_user_info():
    token = request.headers.get('Authorization')
    print("token值{}".format(token))
    info = de_token(token)
    print("info的值{}".format(info))
    info_json = json.dumps(info["id"], sort_keys=True, indent=4)
    return info_json, 200




