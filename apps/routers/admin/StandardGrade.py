"""
导入评分标准
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models import mydb
from json import dumps
standardGrade = Blueprint('standardGrade_bp', __name__, url_prefix='/api/v1')
my_col = mydb['match']
my_admin = mydb['admin']
my_users = mydb['users_copy1']
my_grade = mydb['standardGrade']

# 导入评分标准详情
@standardGrade.route('/standardGrade', methods=['POST'])
@jwt_required
def user_score():
    try:
        standard = request.args['standard']
        sex = request.args['sex']
        projectname = request.args['projectname']
        print(standard)
        data = request.json['data']
        data111 = my_grade.find_one({"standard": standard,"sex": sex,"projectname": projectname})
        print(data111)
        # 保存总分值
        score = []
        # 保存成绩
        grade = []
        all_name = []
        # 判断输入的excel表格那行有错
        i = 0
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if data111 == None :
                for line in data:
                    # 判断第几行出错
                    i = i + 1
                    values = tuple(line.values())
                    it = iter(values)
                    for j in range(1, len(values)):
                        if next(it) == "":
                            baocuo = "当前行错误，错误行为：" + str(i)
                            return jsonify(
                                {'success': False, 'message': baocuo}), 200
                    if line['score'] != '':
                        score.append(line['score'])
                    else:
                        continue
                    if line['score'] != "":

                        grade.append(round(line['grade'],4))
                    else:
                        continue
                print(grade)
                if len(score) != len(grade):
                    return jsonify({'success': False,
                                    'message': 'The score is inconsistent with the number of grades'}), 401
                my_grade.insert_one(
                    {"standard": str(standard), "sex": sex, "projectname": str(projectname), "grade": grade, "score": score})
                return jsonify({'status': 'Event released successfully'}), 200
            else:
                for line in data:
                    # 判断第几行出错
                    i = i + 1
                    values = tuple(line.values())
                    it = iter(values)
                    for j in range(1, len(values)):
                        if next(it) == "":
                            baocuo = "当前行错误，错误行为：" + str(i)
                            return jsonify(
                                {'success': False, 'message': baocuo}), 200
                    if line['score'] != '':
                        score.append(line['score'])
                    else:
                        continue
                    if line['score'] != "":

                        grade.append(round(line['grade'], 4))
                    else:
                        continue
                print(grade)
                if len(score) != len(grade):
                    return jsonify({'success': False,
                                    'message': 'The score is inconsistent with the number of grades'}), 401
                my_grade.update_one({"standard": str(standard), "sex": sex, "projectname": str(projectname)},
                                    {"$set":{"standard": str(standard), "sex": sex, "projectname": str(projectname), "grade": grade, "score": score}})
                return jsonify({'status': 'Event released successfully'}), 200

        else:
            return jsonify({'success': False,
                            'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of keys entered'}), 401
    except ValueError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 401

# 删除评分标准
@standardGrade.route('/standardGrade', methods=['DELETE'])
@jwt_required
def delete_score():
    data = []
    try:
        # 判断请求数据的长度
        data1 = list(request.json.values())
        print(data1)
        event_data = []
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 3:
                return jsonify({'success': False,
                                'message': 'Wrong number of values entered'}), 401
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Wrong number of values entered'}), 401
                else:
                    my_grade.delete_one({"standard": request.json['standard'], "sex": request.json['sex'],
                                         "projectname": request.json['projectname']})
                    return jsonify({'status': 'Event delete successfully'}), 200
        else:
            return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 401



# 获取评分标准是否已有标准
@standardGrade.route('/getstandardGrade', methods=['GET'])
@jwt_required
def get_standardgrade():
    standard = request.args['standard']
    sex = request.args['sex']
    projectname = request.args['projectname']
    grade_data = []
    sex_all = ['男','女']
    if sex not in sex_all:
        return jsonify({'status': '请输入正确的性别'}), 200
    for match_data in my_grade.find():
        grade_data.append(
            {"standard": match_data['standard'], "sex": match_data['sex'],
             "projectname": match_data['projectname']})
    if my_admin.find_one({'Admin_email': get_jwt_identity()}):
        if {"standard": standard, "sex": sex, "projectname": projectname} in grade_data:
            all_grade = "1"
            all_score = "1"
            all_grade = my_grade.find_one({"standard": standard, "sex": sex, "projectname": projectname})['grade']
            all_score = my_grade.find_one({"standard": standard, "sex": sex, "projectname": projectname})['score']
            return dumps({"all_grade": all_grade, "all_score": all_score}), 200
        else:

            return dumps({"all_grade": "1", "all_score": "1"}), 200
    else:
        return jsonify(
                {'success': False, 'message': 'The current user does not exist and cannot perform the operation'}), 401

# 添加自定义标准
@standardGrade.route('/add_public', methods=['POST'])
@jwt_required
def release_match():
    try:
        # data包含了要添加的赛事名称，地点，内容，时间
        data = [{"standard": request.json['standard'], "sex": request.json['sex'],
                 "projectname": request.json['projectname'], "grade":[], "score":[]}]
        # 判断请求数据的长度
        print(data)
        data1 = list(request.json.values())
        # 判断数据库是否已有相同标准
        if my_grade.find_one({"standard": request.json['standard'], "sex": request.json['sex'],
                 "projectname": request.json['projectname']}) is not None:
            standard = "1"
        else:
            standard = ""
        # 判断当前用户是否是管理员
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            if len(data1) != 3:
                return jsonify({'success': False,
                                'message': 'Please enter the event information to be created correctly'}), 200
            else:
                if '' in data1:
                    return jsonify({'success': False,
                                    'message': 'Please enter the event information to be created correctly'}), 200
                if standard != "" :
                    return jsonify({'success': False,
                                    'message': 'The event already exists'}), 401
                else:
                    my_grade.insert(data[0])
                    return jsonify({'status': 'Event released successfully'}), 200

        else:
            return jsonify({'success': False,
                            'message': 'The current user does not exist and cannot perform the operation'}), 200
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Wrong number of keys entered'}), 200
    except ValueError:
        return jsonify({'success': False,
                        'message': 'Wrong number of values entered'}), 200

# 查看标准名
@standardGrade.route('/standard_sportsQuery', methods=['GET'])
@jwt_required
def get_standent_apply():
    user_data = []
    match_data = []
    for grade_message in my_grade.find():
        match_data.append({"standard": grade_message['standard'], "sex": grade_message['sex'],
                           "projectname": grade_message['projectname']})
    user_data.append({"match_data":match_data})
    # 获取用户要页码
    try:
        # new_page = request.args["page"]
        # pager = Pager(int(new_page))
        # if int(new_page) == 0:
        #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        print(get_jwt_identity())
        # 判断当前用户在数据库中是否存在
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            return dumps(user_data), 200
            # if pager.start <= len(match_data):
            #     if pager.end <= len(match_data):
            #         user_data.append({"user_data_f":match_data[pager.start:pager.end]})
            #         return dumps(user_data), 200
            #     else:
            #         user_data.append({"user_data_f":match_data[pager.start:]})
            #         return dumps(user_data), 200
            # else:
            #     print(1)
            #     return jsonify({'success': False, 'message': 'The page number you requested does not exist'}), 401
        else:
            print(2)
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        print(3)
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        print(4)
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401




#查询原始成绩与得分对照表
@standardGrade.route('/relativeGrade', methods=['GET'])
@jwt_required
def get_Relativegrade():
    try:
        all_grade = []
        user_one_grade = []
        print(request.args['standard'], request.args['sex'], request.args['projectname'])
        # 判断当前用户在数据库中是否存在
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):

            user_one_grade = my_grade.find_one({"standard": request.args['standard'], "sex": request.args['sex'],
                 "projectname": request.args['projectname']})['grade']
            fingrade= my_grade.find_one({"standard": request.args['standard'], "sex": request.args['sex'],
                 "projectname": request.args['projectname']})['score']      
            i = 1
            print(fingrade)
            if user_one_grade != []:
                for grade_data in user_one_grade:
                    all_grade.append(
                        {"grade1": round(grade_data, 4), 
                        "num": i,
                        "fingrade":round(fingrade[i-1], 4)
                        })


                    i = i + 1
                return dumps(all_grade), 200
            else:
                return dumps(all_grade), 200
        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401




# 查看具体成绩
@standardGrade.route('/grade_sportsQuery', methods=['GET'])
@jwt_required
def get_grade_apply():
    try:
        all_grade = []
        user_one_grade = []
        print(request.args['standard'], request.args['sex'], request.args['projectname'])
        # 判断当前用户在数据库中是否存在
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):

            user_one_grade = my_grade.find_one({"standard": request.args['standard'], "sex": request.args['sex'],
                 "projectname": request.args['projectname']})['grade']
            i = 1
            if user_one_grade != []:
                for grade_data in user_one_grade:
                    all_grade.append({"grade1": round(grade_data, 4), "num": i})
                    i = i + 1
                return dumps(all_grade), 200
            else:
                return dumps(all_grade), 200
        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401

# 查看具体分数
@standardGrade.route('/score_sportsQuery', methods=['GET'])
@jwt_required
def get_score_apply():
    try:
        all_score = []
        user_one_score = []
        # 判断当前用户在数据库中是否存在
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            user_one_score = my_grade.find_one({"standard": request.args['standard'], "sex": request.args['sex'],
                                                "projectname": request.args['projectname']})['score']
            i = 1
            if user_one_score != []:
                for score_data in user_one_score:
                    all_score.append({"score1": round(score_data, 4), "num": i})
                    i = i + 1
                return dumps(all_score), 200
            else:
                return dumps(all_score), 200
        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401


# 获取标准名全部信息
@standardGrade.route('/get_standard', methods=['GET'])
@jwt_required
def standard_apply():
    try:
        all_standard = []
        all_standard1 = []
        # 判断当前用户在数据库中是否存在
        if my_admin.find_one({'Admin_email': get_jwt_identity()}):
            for standard in my_grade.find():
                print(standard)
                all_standard.append(standard['standard'])
            print(all_standard)
            all_standard = list(set(all_standard))
            for one_standard in all_standard:
                all_standard1.append({"label": one_standard, "value": one_standard})
            print(all_standard1)
            return dumps(all_standard1), 200
        else:
            return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401


# 编辑标准
@standardGrade.route('/alterstandent', methods=['PUT'])
@jwt_required
def alter_standent_apply():
    try:
        sex_all = ['男', '女']
        if request.json['new_sex'] not in sex_all:
            return jsonify({'status': '请输入正确的性别'}), 200
        else:
            # 判断当前用户在数据库中是否存在
            if my_admin.find_one({'Admin_email': get_jwt_identity()}):
                my_grade.update_one({"standard": str(request.json['standard']), "sex": request.json['sex'],
                                     "projectname": str(request.json['projectname'])}, {
                                        "$set": {"standard": str(request.json['new_standard']),
                                                 "sex": str(request.json['new_sex']),
                                                 "projectname": str(request.json['new_projectname'])}})
                return jsonify({'status': 'Event modify successfully'}), 200
            else:
                return jsonify({'success': False, 'message': 'Insufficient permissions of current account'}), 401
    except KeyError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401
    except ValueError:
        return jsonify({'success': False, 'message': 'Wrong number of values entered'}), 401

"""
分页
这个分页的功能包括
1、根据用户请求当前页和总数据条数计算出m和n
2、根据m和n去数据中取数据
而使用property属性就可以满足需求
直接函数调用start和end就可以知道取的开始页还有结束页
"""


class Pager:
    def __init__(self, current_page):
        self.current_page = current_page
        # 规定每一页的个数
        self.per_items = 5

    @property
    def start(self):
        val = (self.current_page-1)*self.per_items
        return val

    @property
    def end(self):
        val = self.current_page*self.per_items
        return val



