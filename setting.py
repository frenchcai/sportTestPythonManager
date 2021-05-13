'''
Author: your name
Date: 2021-02-05 15:39:42
LastEditTime: 2021-02-10 22:31:17
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \sportBackd:\实习\北数科\学习心得\体育后台\接口\sports_Backend\setting.py
'''
class Config:
    DEBUG = True
    TESTING = True
    JWT_SECRET_KEY = 'Super_Secret_JWT_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

# class ProductionConfig(Config):


class TestingConfig(Config):
    TESTING = True
