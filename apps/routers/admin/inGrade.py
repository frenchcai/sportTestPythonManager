#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : yunze
"""
导入比赛成绩
"""
from flask import current_app,Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from pymongo import UpdateOne, ReplaceOne
import datetime
import pandas
inGrade = Blueprint('grade_bp', __name__, url_prefix='/api/v1')


my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']
my_grade = mydb['standardGrade']

# 导入比赛成绩


@inGrade.route('/inGrade', methods=['POST'])
@jwt_required
def import_match():
    current_app.logger.info("this is info")
    try:
        current_app.logger.info("this is info")
        if len(request.json.keys()) < 2:
            baocuo = "未选中评分标准"
            return jsonify(
                {'success': False, 'message': baocuo}), 200
        # 保存标准
        current_app.logger.info("this is info")
        data_standard = []
        data = request.json['gradeAll']
        standard1 = request.json['standard']
        #project_name 比赛名称
        project_name = request.args["name"]
        event_time = request.args["time"]
        site = request.args["site"]
        # 保存更新到用户集合的数据
        arr = []
        # 保存到比赛集合的数据
        arr1 = []
        # 判断输入的excel表格那行有错
        i = 0
        current_app.logger.info("this is info")
        user_score = []
        user_grade = []
        current_app.logger.info('grolsh')
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            #data--表格原始数据
            for line in data:
                i = i+1
                for standard in my_grade.find():
                    biaozhun = str(
                        standard['standard']) + str(standard['sex']) + str(standard['projectname'])
                    standard_data = str(standard1) + \
                        str(line['sex'])+str(line['project'])
                    if biaozhun == standard_data:
                        user_score = standard['score']
                        user_grade = standard["grade"]

                print(6)
                if user_grade == [] or user_score == []:
                    baocuo = "标准未上传，为：" + \
                        str(standard1)+"," + \
                        str(line['sex'])+","+str(line['project'])
                    return jsonify(
                        {'success': False, 'message': baocuo}), 200
                user_data_project = []
                match_data_persion = []
                user_one_project = []
                # values获取值
                values = tuple(line.values())
                it = iter(values)
                # for j in range(1, len(values)):
                #     if next(it) == "":
                #         baocuo = "当前行错误，错误行为：" + str(i)
                #         return jsonify(
                #             {'success': False, 'message': baocuo}), 200
                # 评分转换
                it1 = iter(user_grade)
                print(7)
                # print(user_score)
                # print(user_grade)
                fingrade = 0
                model=0

                #成绩从大到小排序
                if(float(user_grade[1])>=float(user_grade[2])):

                    if(float(user_score[1])>=float(user_score[2])):
                        #成绩越小，分越低
                        model=1

                    elif(float(user_score[1])<float(user_score[2])):
                        #成绩越小，分越高
                        model=2

                #成绩从小到大排序
                else:
                    if(float(user_score[1])>=float(user_score[2])):
                        #成绩越大，分越低
                        model=3

                    elif(float(user_score[1])<float(user_score[2])):
                        #成绩越大，分越高
                        model=4
                print(model,"model")
                for j in range(0,len(user_grade)):
                    #成绩从大到小排序
                    if(model==1):
                        #成绩越小，分越低
                        if(float(line['grade'])<float(user_grade[j])):
                            if(j==(len(user_grade)-1)):
                                fingrade=0
                                break
                            continue

                        elif(float(line['grade'])==float(user_grade[j])):
                            fingrade=user_score[j]
                            break
                            
                        else:
                            if(j==0):
                                fingrade=user_score[0]
                                break
                            else:
                                gradeGap=float(user_grade[j-1])-float(user_grade[j])
                                scoreGap=float(user_score[j-1])-float(user_score[j])
                                fingrade=float(user_score[j-1])-(float(scoreGap/gradeGap)*(float(user_grade[j-1])-float(line['grade'])))
                                break


                    elif(model==2):
                        #成绩越小，分越高
                        print("model,成绩越小，分越高")
                        if(float(line['grade'])<float(user_grade[j])):
                            if(j==(len(user_grade)-1)):
                                fingrade=user_score[j]
                                break
                            continue
                        
                        elif(float(line['grade'])==float(user_grade[j])):
                            fingrade=user_score[j]
                            break
                        else:
                            print("转换完成",j,float(line['grade'])==float(user_grade[j]))
                            if(j==0):
                                fingrade=0
                                break

                        
                            else:
                                gradeGap=float(user_grade[j-1])-float(user_grade[j])
                                scoreGap=float(user_score[j])-float(user_score[j-1])
                                fingrade=float(user_score[j])-(float(scoreGap/gradeGap)*(float(line['grade'])-float(user_grade[j])))
                                break

                            

                    elif(model==3):
                        #成绩越大，分越低
                        if(float(line['grade'])>float(user_grade[j])):
                            if(j==(len(user_grade)-1)):
                                fingrade=0
                                break
                            continue

                        elif(float(line['grade'])==float(user_grade[j])):
                            fingrade=user_score[j]
                            break

                        else:
                            if(j==0):
                                fingrade=user_score[0]
                                break
                            else:
                                gradeGap=float(user_grade[j])-float(user_grade[j-1])
                                scoreGap=float(user_score[j-1])-float(user_score[j])
                                fingrade=float(user_score[j-1])-(float(scoreGap/gradeGap)*(float(line['grade'])-float(user_grade[j-1])))
                                break

                            

                        
                    else:
                        #成绩越大，分越高
                        if(float(line['grade'])>float(user_grade[j])):
                            if(j==(len(user_grade)-1)):
                                fingrade=user_score[j]
                                break
                            continue
                        elif(float(line['grade'])==float(user_grade[j])):
                            fingrade=user_score[j]
                            break
                        else:
                            if(j==0):
                                fingrade=0
                                break;
                            else:
                                gradeGap=float(user_grade[j])-float(user_grade[j-1])
                                scoreGap=float(user_score[j])-float(user_score[j-1])
                                fingrade=float(user_score[j])-(float(scoreGap/gradeGap)*(float(user_grade[j])-float(line['grade'])))
                                break




                        


                
     
                print("转换完成")                    
                fingrade=round(fingrade,2)


                # for j in range(i-1, len(user_grade)):
                #     floata = next(it1)
                #     print(i, j, floata)

                #     if float(user_grade[1]) < float(user_grade[2]):
                #         #原始成绩从小到大
                #         if user_score[1] < user_score[2]:
                #             if float(line['grade']) < float(round(floata, 2)):
                #                 print(1110)
                #                 if j == 0:
                #                     fingrade = user_score[j]
                #                     print(fingrade)
                #                     break
                #                 else:
                #                     fingrade = user_score[j - 1]
                #                     print(fingrade)
                #                     break
                #             if float(line['grade']) >= user_grade[len(user_grade) - 1]:
                #                 fingrade = user_score[len(user_grade) - 1]
                #                 print(fingrade)
                #                 break
                #         else:
                #             if float(line['grade']) <= float(round(floata, 2)):
                #                 print(1110)
                #                 if j == 0:
                #                     fingrade = user_score[j]
                #                     print(fingrade)
                #                     break
                #                 else:
                #                     fingrade = user_score[j]
                #                     print(fingrade)
                #                     break
                #             if float(line['grade']) >= user_grade[len(user_grade) - 1]:
                #                 fingrade = user_score[len(user_grade) - 1]
                #                 print(fingrade)
                #                 break
                #     else:
                #         #原始成绩从大到小
                #         if user_score[1] < user_score[2]:
                #             #成绩越小，分数越高
                #             if float(line['grade']) >= float(round(floata, 2)):
                #                 print(1110)
                #                 if j == 0:
                #                     fingrade = user_score[j]
                #                     print(fingrade)
                #                     break
                #                 else:
                #                     fingrade = user_score[j]
                #                     print(fingrade)
                #                     break
                #             if float(line['grade']) <= user_grade[len(user_grade) - 1]:
                #                 fingrade = user_score[len(user_grade) - 1]
                #                 print(fingrade)
                #                 break
                #         else:
                #             #成绩越小，分数越低
                #             if user_score[1] < user_score[2]:
                #                 if float(line['grade']) >= float(round(floata, 4)):
                #                     print(1110)
                #                     if j == 0:
                #                         fingrade = user_score[j]
                #                         print(fingrade)
                #                         break
                #                     else:
                #                         fingrade = user_score[j]
                #                         print(fingrade)
                #                         break
                #                 if float(line['grade']) <= user_grade[len(user_grade) - 1]:
                #                     fingrade = user_score[len(user_grade) - 1]
                #                     print(fingrade)
                #                     break
                #             else:
                #                 if float(line['grade']) >= float(round(floata, 2)):
                #                     print(1110)
                #                     if j == 0:
                #                         fingrade = user_score[j]
                #                         print(fingrade)
                #                         break
                #                     else:
                #                         fingrade = user_score[j]
                #                         print(fingrade)
                #                         break
                #                 if float(line['grade']) <= user_grade[len(user_grade) - 1]:
                #                     fingrade = user_score[len(user_grade) - 1]
                #                     print(fingrade)
                #                     break





                user_data = my_users.find_one(
                    {"wxId": str(line['id'])})['project'] #个人的所有比赛
                print(8)
                for item in user_data:
                    print(1, item)
                    if str(project_name) == str(item['project_name']):
                        print(99)
                        for user_one_data in item['item']:#比赛的所有项目
                            print(10)
                            if str(line['project']) == user_one_data['item_name']:
                                print(11)
                                # item['company'] = line['unit']
                                # item['group'] = line['group']
                                user_one_project.append({
                                    "wayNumber":user_one_data['wayNumber'], 
                                                        "identifier": str(line['id']),
                                                         "grouping":user_one_data['grouping'],
                                                         "item_cost": user_one_data['item_cost'],
                                                         "item_name": line['project'], 
                                                         "games": user_one_data['games'],
                                                         "serialNumber": user_one_data['serialNumber'], "rank": user_one_data['rank'],
                                                         "item_time": user_one_data['item_time'],
                                                         "session": user_one_data['session'], 
                                                         "fingrade": fingrade,
                                                         "grade": line['grade']
                                                         })
                                print(12)
                            else:
                                user_one_project.append(user_one_data)
                        # 去除重复的字典元素
                        seen = set()
                        new_l = []
                        for d in user_one_project:
                            t = tuple(d.items())
                            if t not in seen:
                                seen.add(t)
                                new_l.append(d)

                        print(new_l)
                        item['item'] = user_one_project
                        user_data_project.append(item)
                        print(user_data_project)
                        print(22141)
                    else:
                        user_data_project.append(item)
                print(user_data_project)


                # 更新user_copy集合
                my_users.replace_one({"name": str(line['name']), "wxId": str(line['id'])},
                                     {"name": str(line['name']), "sex": line['sex'],
                                      "idNumber": my_users.find_one({"wxId": str(line['id'])})['idNumber'],
                                      "phone": my_users.find_one({"wxId": str(line['id'])})['phone'],
                                      "wxId": my_users.find_one({"wxId": str(line['id'])})['wxId'],
                                      "school": my_users.find_one({"wxId": str(line['id'])})['school'],
                                      "project": user_data_project})
                print(4)
                match_data = my_col.find_one(
                    {"project_name": project_name, "event_time": event_time, "site": site})["item"]
                match_one_persion = []
                print(2)

                for item in match_data:
                    if item == line['project']:
                        all_man = match_data[item]["specific_personnel"]
                        # all_man是该项目所有报名用户信息
                        for one_man in all_man:
                            if str(line['id']) == one_man['wxid']:
                                match_one_persion.append(
                                    {"wxid": one_man['wxid'],
                                     "name": str(one_man['name']),
                                    #  "unit": one_man['unit'],
                                     "group": one_man['group'],
                                      "games": one_man['games'],
                                      "gameSession": one_man['gameSession'],
                                     "divGroup": one_man['divGroup'],
                                      "number": one_man['number'],
                                      "identifier": one_man['identifier'],
                                     "sex": one_man['sex'],
                                       "remark": one_man['remark'],
                                     "school": one_man['school'],
                                     "phone": one_man['phone'],
                                     "idNumber": one_man['idNumber'],
                                     "wayNumber": one_man['wayNumber'],
                                     "serialNumber":one_man['serialNumber'],
                                    #  "wayNumber": line['wayNumber'],
                                     "grade": str(line['grade']),
                                     "fingrade": fingrade})
                            else:
                                match_one_persion.append(one_man)
                        match_data[item]['specific_personnel'] = match_one_persion
                        print(79669)
                        allw = match_data[item]
                        print(allw)
                        match_data_persion.append({item: allw})
                        print(match_data_persion)
                    else:
                        match_data_persion.append({item: match_data[item]})
                match_all_data_persion = {}
                for match_one_data_persion in match_data_persion:
                    print(match_one_data_persion.values())
                    match_all_data_persion[list(match_one_data_persion.keys())[0]] = \
                        list(match_one_data_persion.values())[0]
                print(3)
                my_col.update_one({"project_name": str(project_name), "event_time": event_time, "site": site},
                                  {"$set": {"project_name": str(project_name), "event_time": event_time,
                                            "site": site, "item": match_all_data_persion,
                                            "content": my_col.find_one({"project_name": str(project_name),
                                                                        "event_time": event_time, "site": site})[
                                      'content']
                                  }})
            #     arr.append(one)
            #     arr1.append(two)
            #     if len(arr1) % 1000 == 0:  # 每次批量插入的数量，1000条插入一次
            #         my_users.bulk_write(arr)
            #         my_col.bulk_write(arr1)
            #         arr = []
            #         arr1 = []
            #         print("num:%d mid: %s" % (len(arr), datetime.datetime.now()))
            #     else:
            #         continue
            # my_users.bulk_write(arr)
            # my_col.bulk_write(arr1)
            return jsonify({'status': 'Event modify successfully'}), 200
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
       
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401
    except ValueError:
        print(2)
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
