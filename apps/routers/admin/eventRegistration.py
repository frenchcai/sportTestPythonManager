"""
赛事报名列表
"""
from flask import Blueprint, jsonify, request
from json import dumps
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from utils import Pager
from utils import is_valid_date
Registration = Blueprint('registration_bp', __name__, url_prefix='/api/v1')
my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']



# 赛事报名列表
@Registration.route('/competitionRegistration', methods=['GET'])
@jwt_required
def competition():
    try:
        # new_page = request.args["page"]
        # pager = Pager(int(new_page))
        # if int(new_page) == 0:
        #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        time = request.args["time"]
        site = request.args["site"]
        name = request.args["name"]
        user_data = []
        print(time,site,name)
        # 保存查询的数据
        one = []
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            for match_message in my_col.find({"event_time": time, "site": site, "project_name": name}):
                item = match_message['item']
                keys = list(item.keys())
                for k in keys:

                    for person in match_message['item'][k]['specific_personnel']:
                        
                        data = {"wxid": person['wxid'], "name": person['name'],
                                "sex": person['sex'],
                                "school": person['school'],
                                "cost":match_message['item'][k]['cost'],
                                "phone": person['phone'],
                                "games":person['games'],
                                "session":person['gameSession'],
                                "group":person['group'],
                                "grouping":person['divGroup'],
                                "serialNumber":person['serialNumber'],
                                "wayNumber":person['wayNumber'],
                                "grade":person['grade'],
                                "competition_time": match_message['item'][k]['competition_time'],
                                "fingrade":person['fingrade'],
                                "idNumber": person['idNumber'], "sname": k}
                        one.append(data)

            user_data.append({"and_data":one})
            return dumps(user_data), 200
            # if pager.start <= len(one):
            #     if pager.end <= len(one):
            #         user_data.append({"user_data_f": one[pager.start:pager.end]})
            #         return dumps(user_data), 200
            #     else:
            #         user_data.append({"user_data_f": one[pager.start:]})

            # else:
            #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
            return jsonify(
                {'success': False, 'message': 'Wrong key entered'}), 401
    except ValueError:
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401
    except AttributeError:
        return jsonify(
            {'success': False, 'message': '暂无项目，请添加'}), 401


# 赛事详情人员信息删除
@Registration.route('/delpublic', methods=['DELETE'])
@jwt_required
def delete_match():
    print(request.json)
    my_col = mydb['match']
    my_admin = mydb['admin']
    # data包含了要添加的赛事名称，地点,时间
    data = []
    try:
        # 判断输入的时间是否正确
        if is_valid_date(request.json['event_time']) == 'yes':
            return jsonify({'success': False,
                            'message': 'Wrong time format entered'}), 401
        # if request.json['crane_match_name'] == "100米":
        #     crane_match_name = "100_meters_list"
        # if request.json['crane_match_name'] == "跳远":
        #     crane_match_name = "long_jump_list"
        # if request.json['crane_match_name'] == "篮球":
        #     crane_match_name = "basketball_list"
        # if request.json['crane_match_name'] == "足球":
        #     crane_match_name = "football_list"
        # if request.json['crane_match_name'] == "铅球":
        #     crane_match_name = "shot_put_list"
        data.append({"project_name": request.json['project_name'], "event_time": request.json['event_time'],
                     "site": request.json['site']})
        # 判断请求数据的长度
        data1 = list(request.json.values())
        print(data1)
        event_data = []
        for match_data in my_col.find():
            event_data.append(
                {"project_name": match_data['project_name'], "event_time": match_data['event_time'],
                 "site": match_data['site']})
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 6:
                return jsonify({'success': False,
                                'message': 'Wrong number of values entered'}), 401
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Wrong number of values entered'}), 401
                if data[0] in event_data:
                    del_data = my_col.find_one({"project_name": request.json['project_name'], "event_time": request.json['event_time'],
                                                "site": request.json['site']})['item']
                    for del_man in del_data[request.json['crane_match_name']]["specific_personnel"]:
                        if ('wxid',request.json['wxid']) in del_man.items():
                            del_man_data = del_man
                            break
                        else:
                            continue
                    del_data[request.json['crane_match_name']]["specific_personnel"].remove(del_man_data)
                    my_col.update_one({"project_name": request.json['project_name'], "event_time": request.json['event_time'],
                                                "site": request.json['site']},{'$set':{"item":del_data}})
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