'''
Author: your name
Date: 2021-02-05 15:39:42
LastEditTime: 2021-02-10 18:43:29
LastEditors: Please set LastEditors
Description: In User Settings Edit()
FilePath: \sportBackd:\实习\北数科\学习心得\体育后台\接口\sports_Backend\run.py
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
from apps import create_app
app = create_app()

if __name__ == '__main__':
    print("2333")
    app.logger.info("00000")
    app.run(debug = True)
    


