#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
"""
用户登陆、注册方面的接口
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from apps.models import mydb
import re
adminLogin = Blueprint('login_bp', __name__, url_prefix='/api/v1')


# 用户登录的接口
@adminLogin.route('/login', methods=['POST'])
def user_login():
    my_col = mydb['admin']
    # data包含用户的邮箱和密码（2个数据）
    data = list(request.json.values())
    print(request.json.values())
    # 判断是否输入了账号和密码

    if len(data) is 2 and '' not in data:
        # 判断用户是否存在
        email_record = my_col.find_one({'Admin_email': data[0]})

        if email_record:
            # 判断根据email和password是否在数据库中找到记录
            user_record = my_col.find_one({'Admin_email': data[0], 'Admin_pwd': data[1]})
            if user_record:
                access_token = create_access_token(identity=data[0])
                return jsonify({'success': True, 'token': access_token}), 200
            else:
                return jsonify({'success': False, 'message': 'Wrong email or password'}), 401
        else:
            return jsonify({'success': False, 'message': 'Current admin does not exist'}), 401
    else:
        return jsonify({'success': False, 'message': 'Please input your email or password'}), 401


@adminLogin.route('/verify_token', methods=['POST'])
@jwt_required
def verify_token():
    return jsonify({'success': True}), 200


@adminLogin.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(name=current_user), 200


# 注销登录
@adminLogin.route('/logout', methods=['POST'])
@jwt_required
def logout():
    return jsonify({"code": 200, "status": "success"}), 200

# 修改密码的接口
@adminLogin.route('/change_password', methods=['POST'])
@jwt_required
def security():
    my_col = mydb['admin']
    # 获取用户要修改的密码
    if request.json["password"] == "":
        return jsonify({'success': False, 'message':
                                '输入的原密码为空，请先输入原密码'}), 200
    if request.json['new_password'] == '':
        return jsonify({'success': False, 'message':
            '输入的新密码为空，请先输入新密码'}), 200
    a = bool(re.search(r'\d', request.json['new_password']))
    b = bool(re.search('[a-z]', request.json['new_password']))
    if (a == False or b == False):
        return jsonify({'success': False, 'message':
            '请重新设置密码，新密码至少要有数字和字符'}), 200
    if len(request.json['new_password']) < 8:
        return jsonify({'success': False, 'message':
            '请重新设置密码，新密码至少要有8位'}), 200
    password = request.json["password"]
    print(password)
    new_password = request.json['new_password']
    # 判断当前用户在数据库中是否存在
    if my_col.find_one({'Admin_email': get_jwt_identity()}):
        old_password = my_col.find_one({'Admin_email': get_jwt_identity()})['Admin_pwd']
        # 判断是否输入了新密码
        if new_password and '' != new_password:
            # 判断新密码和旧密码是否不一样
            if old_password != new_password and password == old_password:
                my_col.update_one(
                    {'Admin_email': get_jwt_identity()}, {
                        "$set": {'Admin_pwd': new_password}
                    }
                )
                return jsonify({'status': 'Password modified successfully'}), 200
            else:
                return jsonify({'success': False, 'message':
                                'The new password is the same as the old one password is no correct'}), 401
        else:
            return jsonify({'success': False, 'message': 'Password cannot be null'}), 401
    else:
        return jsonify({'success': False, 'message': 'Current admin does not exist'}), 401
