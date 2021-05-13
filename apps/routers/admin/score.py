"""
查看某用户成绩
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from json import dumps
grade1 = Blueprint('garde1_bp', __name__, url_prefix='/api/v1')
my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']

# 查询用户成绩详情接口
@grade1.route('/score', methods=['GET'])
@jwt_required
def user_score():
    try:
        wxid = request.args['wxid']
        project_name = request.args['project_name']
        # 保存要输出的数据
        arr = {}
        arr1 = []
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            arr = my_col.find_one({'project_name': project_name})['item']
            keys = list(arr.keys())
            print(111)
            if (my_users.find_one({"wxId": wxid}) == None):
                return dumps(arr1), 200
            else:
                projects = my_users.find_one({"wxId": wxid})["project"]
                for project in projects:
                    if project_name == project['project_name']:
                        company = project['company']
                        break
                for key in keys:
                    items = arr[key]['specific_personnel']
                    print(22)
                    for item in items:
                        if item['wxid'] == wxid:
                            print(333)
                            arr1.append({"name": item['name'], "wayNumber": item['wayNumber'], "competition": key,
                                         "identifier": item['identifier'], "company": company,
                                         "grade": item['grade'], "fingrade": item['fingrade'],
                                         "remarks": item['remark']})
                        else:
                            continue
                print(arr1)
                return dumps(arr1), 200
    except KeyError:
        return jsonify(
            {'success': False, 'message': 'Wrong key entered'}), 401
    except ValueError:
        return jsonify(
            {'success': False, 'message': 'Wrong value entered'}), 401



