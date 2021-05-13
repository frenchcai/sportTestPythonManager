'''
Author: your name
Date: 2021-02-05 15:39:42
LastEditTime: 2021-02-05 19:11:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \sportBackd:\实习\北数科\学习心得\体育后台\接口\sports_Backend\apps\routers\users\personInfo.py
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
"""
个人信息
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource, Api
# personInfo = Blueprint('personInfo_bp', __name__, url_prefix='/api/v1')
# api = Api(personInfo)




class Info(Resource):
    @staticmethod
    def get():
        return {'hello': 'world'}

    @staticmethod
    def post():
        return {'msg': 'post hello world'}


api.add_resource(Info, '/test')
