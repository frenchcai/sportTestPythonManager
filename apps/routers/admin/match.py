"""
赛事接口
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from utils import Pager
from json import dumps
from pymongo import UpdateOne,ReplaceOne
from utils import is_valid_date
import re
matchevent = Blueprint('match_bp', __name__, url_prefix='/api/v1')

# 赛事发布接口
@matchevent.route('/public', methods=['POST'])
@jwt_required
def release_match():
    my_col = mydb['match']
    my_admin = mydb['admin']
    try:
        # 判断输入的时间是否正确
        if is_valid_date(request.json['time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 200
        # data包含了要添加的赛事名称，地点，内容，时间
        data = [{"name": request.json['name'], "time": request.json['time'],
                 "site": request.json['site'],
                 "content": request.json['content']}]
        # 判断请求数据的长度
        data1 = list(request.json.values())
        event_data = []
        for match_data in my_col.find():
            event_data.append(
                {"name": match_data['project_name'], "time": match_data['event_time'],
                 "site": match_data['site'],
                 "content": match_data['content']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 4:
                return jsonify({'success': False,
                                'message': 'Please enter the event information to be created correctly'}), 200
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Please enter the event information to be created correctly'}), 200
                if data[0] not in event_data:
                    my_col.insert(
                        {
                            "project_name": str(request.json['name']),
                            "event_time": request.json['time'],
                            "site": request.json['site'],
                            "content": request.json['content'],
                            "item": {}
                        })
                    return jsonify({'status': 'Event released successfully'}), 200
                else:
                    return jsonify({'success': False,
                                    'message': 'The event already exists'}), 401
        else:
            return jsonify({'success': False,
                            'message': 'The current user does not exist and cannot perform the operation'}), 200
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of keys entered'}), 200
    except ValueError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 200

# 赛事删除
@matchevent.route('/public', methods=['DELETE'])
@jwt_required
def delete_match():
    my_col = mydb['match']
    my_admin = mydb['admin']
    print(request.json)
    # data包含了要添加的赛事名称，地点,时间
    data = []
    try:
        # 判断输入的时间是否正确
        if is_valid_date(request.json['time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 401
        data.append({"name": request.json['name'], "time": request.json['time'],
                     "site": request.json['site']})
        # 判断请求数据的长度
        data1 = list(request.json.values())
        event_data = []
        for match_data in my_col.find():
            event_data.append(
                {"name": match_data['project_name'], "time": match_data['event_time'],
                 "site": match_data['site']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 3:
                return jsonify({'success': False,
                                'message': 'Wrong number of values entered'}), 401
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Wrong number of values entered'}), 401
                if data[0] in event_data:
                    my_col.delete_one(
                        {'project_name': data1[0], "event_time": data1[1], "site": data1[2]})

                    return jsonify({'status': 'Event delete successfully'}), 200
                else:
                    return jsonify({'success': False,
                                    'message': 'The event already not exists'}), 401
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 401


# 赛事查询
@matchevent.route('/sportsQuery', methods=['GET'])
@jwt_required
def get_match_apply():
    # 获取管理员信息
    my_col = mydb['admin']
    # 获取赛事信息
    my_col_match = mydb['match']
    user_data = []
    match_data = []
    for match_message in my_col_match.find():
        match_data.append({"name": match_message['project_name'], "time": match_message['event_time'],
                           "site": match_message['site'], "content": match_message['content']})
    user_data.append({"match_data":match_data})
    # 获取用户要页码
    try:
        # new_page = request.args["page"]
        # pager = Pager(int(new_page))
        # if int(new_page) == 0:
        #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        # 判断当前用户在数据库中是否存在
        if my_col.find_one({'Admin_email': get_jwt_identity()}):
            return dumps(user_data), 200
            return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
            # if pager.start <= len(match_data):
            #     if pager.end <= len(match_data):
            #         user_data.append({"user_data_f":match_data[pager.start:pager.end]})
            #         return dumps(user_data), 200
            #     else:
            #         user_data.append({"user_data_f":match_data[pager.start:]})


        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401

# 赛事修改
@matchevent.route('/public', methods=['PUT'])
@jwt_required
def alter_match_apply():
    my_col = mydb['match']
    my_admin = mydb['admin']
    my_user = mydb['users_copy1']
    # data包含了要添加的赛事名称，地点，内容，时间
    data = []
    try:
        # 判断输入的时间格式是否正确
        if is_valid_date(request.json['time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 401
        name = request.json['name']
        data.append({"name":name , "time": request.json['time'],
                     "site": request.json['site']})
        # 获取请求数据的值
        data1 = list(request.json.values())
        del data1[0:3]
        # 获取请求数据的键
        data2 = list(request.json.keys())
        # 要删除的key
        delete_key = ['name', 'time', 'site']
        # 如果有要修改的时间，则判断其格式是否正确
        if 'new_time' in data2:
            if is_valid_date(request.json['new_time']) =='yes':
                return  jsonify({'success': False,
                                'message': 'Wrong time format entered'}), 401
        # 获取要修改的键值
        data2 = [x for x in data2 if x not in delete_key]
        # data_k也是获取请求参数的键值
        data_k = []
        for x in data2:
            if x == 'new_time':
                data_k.append(re.sub(r'new_', r'event_', x))
            elif x == 'new_name':
                data_k.append(re.sub(r'new_', r'project_', x))
            else:
                data_k.append(re.sub(r'new_', '', x))
        print(data_k)
        print(data1)
        event_data = []
        arr = []
        for match_data in my_col.find():
            event_data.append(
                {"name": match_data['project_name'], "time": match_data['event_time'],
                 "site": match_data['site']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if data[0] not in event_data:
                return jsonify({'success': False,
                                'message': 'The event already not exists'}), 401
            else:
                if len(data_k) == 0:
                    return jsonify({'status': 'Event modify successfully'}), 200
                if len(data_k) == 1:
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']}, {"$set": {data_k[0]: data1[0]}})
                    return jsonify({'status': 'Event modify successfully'}), 200
                elif len(data_k) == 2:
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']}, {"$set": {data_k[0]: data1[0], data_k[1]: data1[1]}})
                    return jsonify({'status': 'Event modify successfully'}), 200
                elif len(data_k) == 3:
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']},
                        {"$set": {data_k[0]: data1[0], data_k[1]: data1[1], data_k[2]: data1[2]}})
                    return jsonify({'status': 'Event modify successfully'}), 200
                elif len(data_k) == 4:
                    print(111)
                    if request.json['name'] != request.json['new_name']:
                        if my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                             "site": request.json['site']})['item'] == []:
                            my_col.update_one(
                                {'project_name': request.json['name'], "event_time": request.json['time'],
                                 "site": request.json['site']}, {
                                    "$set": {data_k[0]: data1[0], data_k[1]: data1[1], data_k[2]: data1[2],
                                             data_k[3]: data1[3]}})
                            return jsonify({'status': 'Event modify successfully'}), 200
                        else:
                            print(22)
                            user = []
                            user_all_data = my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                                             "site": request.json['site']})['item']
                            if user_all_data == {}:
                                print(33)
                                my_col.update_one(
                                    {'project_name': request.json['name'], "event_time": request.json['time'],
                                     "site": request.json['site']}, {
                                        "$set": {data_k[0]: data1[0], data_k[1]: data1[1], data_k[2]: data1[2],
                                                 data_k[3]: data1[3]}})
                                return jsonify({'status': 'Event modify successfully'}), 200
                            else:
                                print(44)
                                for key in my_col.find_one(
                                        {'project_name': request.json['name'], "event_time": request.json['time'],
                                         "site": request.json['site']})['item']:
                                    person_data = user_all_data[key]['specific_personnel']
                                    for person in person_data:
                                        user_all_project = \
                                            my_user.find_one({"name": person['name'], "wxId": person['wxid']})[
                                                'project']
                                        if user_all_project != []:
                                            for user_project in user_all_project:
                                                if request.json['name'] == user_project['project_name']:
                                                    user.append(
                                                        {"project_name": request.json['new_name'],
                                                         "time": user_project['time'],
                                                         "site": user_project['site'], "group": user_project['group'],
                                                         "company": user_project['company'],
                                                         "remarks": user_project['remarks'],
                                                         "registration_time": user_project['registration_time'],
                                                         "paid": user_project['paid'], "item": user_project['item']})
                                                    print(33)
                                                else:
                                                    user.append(user_project)
                                            my_user.update_one({"name": person['name'],
                                                                "wxId": person['wxid']},
                                                               {"$set":
                                                                    {"project": user}})
                                            my_col.update_one(
                                                {'project_name': request.json['name'],
                                                 "event_time": request.json['time'],
                                                 "site": request.json['site']}, {
                                                    "$set": {data_k[0]: data1[0], data_k[1]: data1[1],
                                                             data_k[2]: data1[2],
                                                             data_k[3]: data1[3]}})
                                            return jsonify({'status': 'Event modify successfully'}), 200
                                        else:
                                            my_col.update_one(
                                                {'project_name': request.json['name'],
                                                 "event_time": request.json['time'],
                                                 "site": request.json['site']}, {
                                                    "$set": {data_k[0]: data1[0], data_k[1]: data1[1],
                                                             data_k[2]: data1[2],
                                                             data_k[3]: data1[3]}})
                                            return jsonify({'status': 'Event modify successfully'}), 200

                    else:
                        my_col.update_one(
                            {'project_name': request.json['name'], "event_time": request.json['time'],
                             "site": request.json['site']}, {
                                "$set": {data_k[0]: data1[0], data_k[1]: data1[1], data_k[2]: data1[2],
                                         data_k[3]: data1[3]}})
                        return jsonify({'status': 'Event modify successfully'}), 200
                else:
                    return jsonify(
                        {'success': False,
                         'message': 'Wrong value entered'}), 401
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except ValueError:
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401
    except KeyError:
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401


# 增加项目名
@matchevent.route('/competition_add_project', methods=['POST'])
@jwt_required
def release_competition():
    event_data = 0
    my_col = mydb['match']
    my_admin = mydb['admin']
    try:
        # 判断输入的时间是否正确
        if is_valid_date(request.json['competition_time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 200
        # data包含了要添加的赛事名称，地点，内容，时间
        data = [{"name": request.json['name'], "time": request.json['time'],
                 "site": request.json['site'], "competition_time":request.json['competition_time'],
                 "competition_name":request.json['competition_name'], "cost":request.json['cost']}]
        # 判断请求数据的长度
        data1 = list(request.json.values())
        # 判断项目名是否在数据库中
        for match_data in my_col.find({"project_name": request.json['name'],"event_time": request.json['time'],
                                       "site": request.json['site']}):
            if request.json['competition_name'] in  match_data['item']:
                event_data = 1
            else:
                continue
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 6:
                return jsonify({'success': False,
                                'message': 'Please enter the event information to be created correctly'}), 200
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Please enter the event information to be created correctly'}), 200
                if event_data == 0:
                    item = my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                                     "site": request.json['site']})['item']
                    if is_number(request.json['cost']) == True:
                        item[request.json['competition_name']] = {"cost": request.json['cost'],
                                                                  "competition_time": request.json['competition_time'],
                                                                  "specific_personnel": []}
                        my_col.update_one(
                            {'project_name': request.json['name'], "event_time": request.json['time'],
                             "site": request.json['site']}, {"$set": {"item": item}})
                        return jsonify({'status': 'Event released successfully'}), 200
                    else:
                        return jsonify({'success': False, 'message': '输入的费用有误，请输入正确的费用（数字）'}), 200
                else:
                    return jsonify({'success': False,
                                    'message': 'The event already exists'}), 401
        else:
            return jsonify({'success': False,
                            'message': 'The current user does not exist and cannot perform the operation'}), 200
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of keys entered'}), 200
    except ValueError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 200

# 查询项目名
@matchevent.route('/competition_sportsQuery', methods=['GET'])
@jwt_required
def get_competition_apply():
    # 获取管理员信息
    my_col = mydb['admin']
    # 获取赛事信息
    my_col_match = mydb['match']
    user_data = []
    competition_details = []
    time = request.args["time"]
    site = request.args["site"]
    name = request.args["name"]
    # 获取全部项目名及信息
    for match_message in my_col_match.find({'project_name': name, "event_time": time,
                                     "site": site}):
        for key in match_message['item']:
            competition_details.append({'competition_name':key,"competition_time":
                match_message['item'][key]['competition_time'], "cost": match_message['item'][key]['cost']})
    user_data.append({"competition_details": competition_details})
    # 获取用户要页码
    try:
        # new_page = request.args["page"]
        # pager = Pager(int(new_page))
        # if int(new_page) == 0:
        #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        # 判断当前用户在数据库中是否存在
        if my_col.find_one({'Admin_email': get_jwt_identity()}):
            return dumps(user_data), 200
            return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
            # if pager.start <= len(competition_details):
            #     if pager.end <= len(competition_details):
            #         user_data.append({"user_data_f":competition_details[pager.start:pager.end]})
            #         return dumps(user_data), 200
            #     else:
            #         user_data.append({"user_data_f":competition_details[pager.start:]})
        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401

# 编辑项目名详情
@matchevent.route('/competition_public', methods=['PUT'])
@jwt_required
def alter_competition_apply():
    my_col = mydb['match']
    my_admin = mydb['admin']
    my_user = mydb['users_copy1']
    # data包含了要添加的赛事名称，地点，内容，时间
    data = []
    try:
        # 判断输入的时间格式是否正确
        if is_valid_date(request.json['new_competition_time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 401
        name = request.json['name']
        data.append({"name": name, "time": request.json['time'],
                     "site": request.json['site']})
        # 获取请求数据的值
        data1 = list(request.json.values())
        del data1[0:4]
        # 获取请求数据的键
        data2 = list(request.json.keys())
        # 要删除的key
        delete_key = ['name', 'time', 'site', 'competition_name']
        # 如果有要修改的时间，则判断其格式是否正确
        if 'new_time' in data2:
            if is_valid_date(request.json['new_time']) == 'yes':
                return jsonify({'success': False,
                                'message': 'Wrong time format entered'}), 401
        # 获取要修改的键值
        data2 = [x for x in data2 if x not in delete_key]
        # data_k也是获取请求参数的键值
        data_k = []
        for x in data2:
            if x == 'new_time':
                data_k.append(re.sub(r'new_', r'event_', x))
            elif x == 'new_name':
                data_k.append(re.sub(r'new_', r'project_', x))
            else:
                data_k.append(re.sub(r'new_', '', x))
        print(data_k)
        print(data1)
        event_data = []
        arr = []
        for match_data in my_col.find():
            event_data.append(
                {"name": match_data['project_name'], "time": match_data['event_time'],
                 "site": match_data['site']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if data[0] not in event_data:
                return jsonify({'success': False,
                                'message': 'The event already not exists'}), 401
            else:
                if len(data_k) == 0:
                    return jsonify({'status': 'Event modify successfully'}), 200
                if len(data_k) == 1:
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']}, {"$set": {data_k[0]: data1[0]}})
                    return jsonify({'status': 'Event modify successfully'}), 200
                elif len(data_k) == 2:
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']}, {"$set": {data_k[0]: data1[0], data_k[1]: data1[1]}})
                    return jsonify({'status': 'Event modify successfully'}), 200
                elif len(data_k) == 3:
                    print(111)
                    if request.json['competition_name'] != request.json['new_competition_name']:
                        user = []
                        all_user_data = []
                        user_all_data = my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']})['item']
                        print(user_all_data)

                        for key in my_col.find_one(
                                {'project_name': request.json['name'], "event_time": request.json['time'],
                                 "site": request.json['site']})['item']:
                            print(333)
                            print(key, 11)
                            if key == request.json['competition_name']:
                                print(444)
                                person_data = user_all_data[key]['specific_personnel']
                                print(person_data,key)
                                if person_data != []:
                                    user_all_name_and_wxId = []
                                    for user_name_and_wxId in my_user.find():
                                        user_all_name_and_wxId.append(
                                            {"name": user_name_and_wxId['name'], "wxId": user_name_and_wxId['wxId']})
                                    print(user_all_name_and_wxId)
                                    for person in person_data:
                                        if ({"name": person['name'], "wxId": person['wxid']}) in user_all_name_and_wxId:
                                            user_all_project = \
                                                my_user.find_one({"name": person['name'], "wxId": person['wxid']})[
                                                    'project']
                                            for user_project in user_all_project:
                                                if request.json['name'] == user_project['project_name']:
                                                    for user_message_data in user_project['item']:
                                                        if request.json['competition_name'] == user_message_data[
                                                            'item_name']:
                                                            user.append(
                                                                {"item_name": request.json['new_competition_name'],
                                                                 "item_time": user_message_data['item_time'],
                                                                 "item_site": user_message_data['item_site'],
                                                                 "rank": user_message_data['rank'],
                                                                 "games": user_message_data['games'],
                                                                 "session": user_message_data['session'],
                                                                 "grouping": user_message_data['grouping'],
                                                                 "serialNumber": user_message_data['serialNumber'],
                                                                 "identifier": user_message_data['identifier'],
                                                                 "wayNumber": user_message_data['wayNumber'],
                                                                 "grade": user_message_data['grade'],
                                                                 "cost": user_message_data['cost']})
                                                        else:
                                                            user.append(user_message_data)
                                                        user_project['item'] = user
                                                    all_user_data.append(user_project)
                                                else:
                                                    all_user_data.append(user_project)

                                            my_user.update_one({"name": person['name'],
                                                                "wxId": person['wxid']},
                                                               {"$set":
                                                                    {"project": all_user_data}})
                                            user_all_data[request.json['competition_name']]['cost'] = request.json[
                                                'new_cost']
                                            user_all_data[request.json['competition_name']]['competition_time'] = \
                                            request.json['new_competition_time']
                                            user_all_data[request.json['new_competition_name']] = user_all_data[
                                                request.json['competition_name']]
                                            del user_all_data[request.json['competition_name']]
                                            my_col.update_one(
                                                {'project_name': request.json['name'],
                                                 "event_time": request.json['time'],
                                                 "site": request.json['site']}, {
                                                    "$set": {"item": user_all_data}})
                                            return jsonify({'status': 'Event modify successfully'}), 200
                                else:
                                    user_all_data[request.json['competition_name']]['cost'] = request.json[
                                        'new_cost']
                                    user_all_data[request.json['competition_name']]['competition_time'] = \
                                        request.json['new_competition_time']
                                    user_all_data[request.json['new_competition_name']] = user_all_data[
                                        request.json['competition_name']]
                                    del user_all_data[request.json['competition_name']]
                                    my_col.update_one(
                                        {'project_name': request.json['name'],
                                         "event_time": request.json['time'],
                                         "site": request.json['site']}, {
                                            "$set": {"item": user_all_data}})
                                    return jsonify({'status': 'Event modify successfully'}), 200


                    else:
                        user_all_data = \
                            my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                                             "site": request.json['site']})['item']
                        user_all_data[request.json['competition_name']]['cost'] = request.json['new_cost']
                        user_all_data[request.json['competition_name']]['competition_time'] = request.json[
                            'new_competition_time']
                        user_all_data[request.json['new_competition_name']] = user_all_data[
                            request.json['competition_name']]
                        del user_all_data[request.json['competition_name']]
                        my_col.update_one(
                            {'project_name': request.json['name'], "event_time": request.json['time'],
                             "site": request.json['site']}, {
                                "$set": {"item": user_all_data}})
                        return jsonify({'status': 'Event modify successfully'}), 200
                else:
                    return jsonify(
                        {'success': False,
                         'message': 'Wrong value entered'}), 401
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except ValueError:
        print(55)
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401
    except KeyError:
        print(666)
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401

# 删除项目名
@matchevent.route('/competition_public', methods=['DELETE'])
@jwt_required
def delete_competition_match():
    my_col = mydb['match']
    my_admin = mydb['admin']
    my_user = mydb['users_copy1']
    print(request.json)
    # data包含了要添加的赛事名称，地点,时间
    data = []
    try:
        # 判断输入的时间是否正确
        if is_valid_date(request.json['time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 401
        data.append({"name": request.json['name'], "time": request.json['time'],
                     "site": request.json['site']})
        # 判断请求数据的长度
        data1 = list(request.json.values())
        event_data = []
        for match_data in my_col.find():
            event_data.append(
                {"name": match_data['project_name'], "time": match_data['event_time'],
                 "site": match_data['site']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 6:
                return jsonify({'success': False,
                                'message': 'Wrong number of values entered'}), 401
            else:
                if data[0] in event_data:
                    user_del_all_data = my_col.find_one({'project_name': request.json['name'], "event_time": request.json['time'],
                                             "site": request.json['site']})['item']
                    for key in user_del_all_data:
                        if key == request.json["del_competition_name"]:
                            user_all_man = user_del_all_data[key]['specific_personnel']
                            del_key = key
                    del user_del_all_data[del_key]
                    user_all_name_and_wxId = []
                    for user_name_and_wxId in my_user.find():
                        user_all_name_and_wxId.append({"name":user_name_and_wxId['name'], "wxId":user_name_and_wxId['wxId']})
                    for user_man in user_all_man:
                        if ({"name": user_man['name'], "wxId": user_man['wxid']}) in user_all_name_and_wxId:
                            user_all_project = \
                                my_user.find_one({"name": user_man['name'], "wxId": user_man['wxid']})[
                                    'project']
                            print(user_all_project)
                            user_del_after_project = []
                            for user_project in user_all_project:
                                if request.json['name'] == user_project['project_name']:
                                    print(222)
                                    for user_message_data in user_project['item']:
                                        if request.json['del_competition_name'] == user_message_data['item_name']:
                                            user_project['item'].remove(user_message_data)
                                            user_del_after_project.append(user_project)
                                        else:
                                            continue
                                else:
                                    user_del_after_project.append(user_project)
                            print(user_del_after_project)
                            my_user.update_one(
                                {"name": user_man['name'], "wxId": user_man['wxid']}, {
                                    "$set": {"project":user_del_after_project}})
                        print(my_user.find_one({"name": user_man['name'], "wxId": user_man['wxid']}))
                    my_col.update_one(
                        {'project_name': request.json['name'], "event_time": request.json['time'],
                         "site": request.json['site']}, {
                            "$set": {"item": user_del_all_data}})

                    return jsonify({'status': 'Event delete successfully'}), 200
                else:
                    return jsonify({'success': False,
                                    'message': 'The event already not exists'}), 401
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 401

# 判断是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False