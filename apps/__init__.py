'''
Author: your name
Date: 2021-02-05 15:39:42
LastEditTime: 2021-02-10 18:53:33
LastEditors: Please set LastEditors
# Description: In User Settings Edit
FilePath: \sportBackd:\实习\北数科\学习心得\体育后台\接口\sports_Backend\apps\__init__.py
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from setting import DevelopmentConfig
from apps.routers import adminLogin, applyinfo, matchevent, apply, register, inArrange, inGrade, Registration, grade1, matcharrange, standardGrade

from logging.config import dictConfig

def create_app():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)
    # 加载配置
    CORS(app)
    JWTManager(app)
    app.config.from_object(DevelopmentConfig)
    # 注册蓝图
    app.register_blueprint(adminLogin)
    app.register_blueprint(applyinfo)
    app.register_blueprint(matchevent)
    # app.register_blueprint(personInfo)
    # app.register_blueprint(apply)
    app.register_blueprint(register)
    app.register_blueprint(inArrange)
    app.register_blueprint(inGrade)
    app.register_blueprint(Registration)
    app.register_blueprint(grade1)
    app.register_blueprint(matcharrange)
    app.register_blueprint(standardGrade)
    return app
