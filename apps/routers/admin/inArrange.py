#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
"""
导入比赛安排
"""
import threading
import time
import pandas
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from pymongo import UpdateOne, ReplaceOne
import datetime
from dateutil.parser import parse
inArrange = Blueprint('arrage_bp', __name__, url_prefix='/api/v1')
my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']

# 考试安排录入


@inArrange.route('/examArrangement', methods=['POST'])
@jwt_required
def release_match():
    try:
        project_name = request.args["name"]
        event_time = request.args["time"]
        site = request.args["site"]
        data = request.json['ArrangeIn']
        # 保存更新到用户集合的数据
        arr = []
        # 保存到比赛集合的数据
        arr1 = []
        arr2 = []
        arr3 = []
        # 判断输入的excel表格那行有错
        i = 0
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            for line in data:
              
                match_data_persion = []
                user_data_project = []
                user_one_project = []
            
                values = tuple(line.values())
                it = iter(values)
                # 判断从前端获取的数据是否有错误的数据
                for j in range(1, len(values)):
                    if next(it) == "":
                        baocuo = "当前行错误，错误行为：" + str(i)
                        return jsonify(
                            {'success': False, 'message': baocuo}), 200


                # 更新到用户里
                user_data = my_users.find_one(
                    {"wxId": str(line['id'])})['project']
                for item in user_data:
              
                    if str(project_name) == str(item['project_name']):
                        for user_one_data in item['item']:
                            if str(line['project']) == user_one_data['item_name']:
                                # group = line['group']
                                # company = line['unit']
                                # remarks = remark
                                grouping = line['divideGroup']
                                serialNumber = line['number']
                                # item_time = time
                                games = line['games']
                                identifier = str(line['id'])
                                item_name = str(line['project'])
                                session = line['session']
                                wayNumber = line['wayNumber']

                                # print(item["project_name"], user_one_data['item_name'])
                                my_users.update_one({"name": str(line['name']), "wxId": str(line['id']),
                                                     "project.project_name": item["project_name"],
                                                     "project.item.item_name": user_one_data['item_name']},

                                                    {'$set': {"project.$[outter].item.$[inner].grouping": grouping,
                                                              "project.$[outter].item.$[inner].serialNumber": serialNumber,
                                                              #   "project.$[outter].item.$[inner].item_time": item_time,
                                                              "project.$[outter].item.$[inner].games": games,
                                                              "project.$[outter].item.$[inner].identifier": identifier,
                                                              "project.$[outter].item.$[inner].item_name": item_name,
                                                              "project.$[outter].item.$[inner].session": session,
                                                              "project.$[outter].item.$[inner].wayNumber": wayNumber,



                                                              }},
                                                    upsert=False,
                                                    array_filters=[{'outter.project_name': item["project_name"]},
                                                                   {'inner.item_name': user_one_data['item_name']
                                                                   }])
                                # my_users.update_one({"name": str(line['name']), "wxId": str(line['id']),
                                #                      "project.project_name": str(project_name)},
                                #                     {"$set": {
                                                        # "project.$.group": group,
                                                        #         "project.$.company": company,
                                                        #         "project.$.remarks": remarks
                                                            #   }})

                print(5555)

                # 更新到赛事集合
                # print(project_name, event_time, site)


                match_data = \
                my_col.find_one({"project_name": str(
                        project_name), "event_time": event_time, "site": site})['item']
                # print(12456)
                match_one_persion = []
                for item in match_data:
                    print(1)
                    print(item, line['project'])
                    if item == line['project']:
                        # match_data[item]['competition_time'] = time
                        print(2)
                        all_man = match_data[item]["specific_personnel"]
                        for one_man in all_man:
                            print(3)
                            if str(line['id']) == one_man['wxid']:
                                one_man['name'] = line['name']
                                # one_man['unit'] = ""
                                # one_man['group'] = ""
                                one_man['gameSession'] = line['session']
                                one_man['games'] = line['games']
                                one_man["divGroup"] = line['divideGroup']
                                one_man['number'] = line['number']
                                # one_man['number'] = line['number']
                                # 道次
                                one_man['serialNumber'] = line['number']
                                one_man['wayNumber'] = line['wayNumber']
                                # one_man['remark'] = ""
                                one_man['identifier'] = str(line['id'])
                                match_one_persion.append(one_man)
                                # print(one_man)
                                print(5)
                            else:
                                match_one_persion.append(one_man)
                        print(3456242)
                        print(match_one_persion)
                        match_data[item]['specific_personnel'] = match_one_persion
                        print(79669)
                        allw = match_data[item]
                        # print(allw)
                        match_data_persion.append({item: allw})
                        # print(match_data_persion)
                    else:
                        match_data_persion.append({item: match_data[item]})
                # print(match_data_persion)
                match_all_data_persion = {}
                for match_one_data_persion in match_data_persion:
                    # print(match_one_data_persion.values())
                    match_all_data_persion[list(match_one_data_persion.keys())[0]] = \
                    list(match_one_data_persion.values())[0]
                # print(1234566363)
                print("字典",match_all_data_persion)
                # 获取要更新的那个字典的所有数据
                my_col.replace_one({"project_name": str(project_name), 
                "event_time": str(event_time),
                 "site": site},
                                   {"project_name": str(project_name), "event_time": str(event_time), "site": site,
                                   "content": my_col.find_one(
                                       {"project_name": str(project_name), "event_time": event_time, "site": site})[
                                       'content'],
                                    "item": match_all_data_persion})
            print("成功更新match")                  

            return jsonify({'status': 'Event modify successfully'}), 200
        else:
            print("找不到")
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401

    except KeyError:
        # print(2)
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401
    except ValueError:
        print(3)
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401
    except TypeError:
        baocuo = "当前行数据没有，没有的数据行为：" + str(i)
        return jsonify({'success': False, 'message': baocuo}), 200


# 定义转化日期戳的函数,stamp为日期戳
def date(stamp):
    delta = pandas.Timedelta(str(stamp)+'D')
    real_time = pandas.to_datetime('1899-12-30') + delta
    return real_time
