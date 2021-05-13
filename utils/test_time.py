"""
验证输入的时间是否正确
"""
from flask import jsonify
import time


def is_valid_date(str_date):
    # 判断是否是一个有效的日期字符串
    try:
        p_time = str_date.split(' ')
        time.strptime(p_time[0], "%Y-%m-%d")
        time.strptime(p_time[1],"%H:%M")
    except ValueError:
        value_time = 'yes'
        return value_time
    except:
        value_time = 'yes'
        return value_time





