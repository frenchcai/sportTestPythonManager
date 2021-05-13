"""
查看某用户赛事安排详情
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from json import dumps
matcharrange = Blueprint('matcharrange_bp', __name__, url_prefix='/api/v1')
my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']


# 查询赛事安排详情接口
@matcharrange.route('/matchInarrage', methods=['GET'])
@jwt_required
def user_score():
    try:
        wxid = request.args['wxid']
        project_name = request.args['project_name']
        # 保存要输出的数据
        arr1 = []
        competition_time = ''
        # 判断当前用户是否是管理员
        company = ''
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            arr = my_col.find_one({'project_name': project_name})['item']
            keys = list(arr.keys())
            if my_users.find_one({"wxId": wxid})== None:
                return dumps(arr1), 200
            else:
                projects = my_users.find_one({"wxId": wxid})["project"]
                for project in projects:
                    print(project)
                    if project_name == project['project_name']:
                        company = project['company']
                        print(company,2345674)
                        break
                # arr = my_users.find_one({'wxId': wxid})['project']
                name = my_users.find_one({'wxId': wxid})['name']
                sex = my_users.find_one({'wxId': wxid})['sex']
                time_data = my_users.find_one({'wxId': wxid})['project']
                for key in keys:
                    items = arr[key]['specific_personnel']
                    for item in items:
                        print(item)
                        if item['wxid'] == wxid:
                            print(2)
                            for time_one_data in time_data:
                                print(3,time_one_data)
                                if (str(time_one_data['project_name']) == str(project_name)):
                                    print(4)
                                    for one_item in time_one_data['item']:
                                        print(5,one_item)
                                        if str(key) == str(one_item['item_name']):
                                            print(6)
                                            competition_time = one_item['item_time']
                                            print(7)
                                        else:
                                            continue
                            print(8)
                            arr1.append(
                                {"name": name, "sex": sex, "group": item['group'], "wayNumber": item['wayNumber'],
                                 "identifier": item['identifier'], "company": company,
                                 "project_name": key,"competition_time":competition_time,
                                 "grouping": item['divGroup']})
                            print(9)
                            competition_time = ''
                        else:
                            continue
                return dumps(arr1), 200
    except KeyError:
        print(11111)
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401
    except ValueError:
        print(222222)
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401