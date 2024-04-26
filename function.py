# -*- encoding:utf-8 -*-
import base64
import json
import requests
from datetime import datetime
from io import BytesIO
import secrets
from db_init import db, app
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Case, TestQuestionPool, Exam, ExamRecord, Case2, Case3, FeeItem, DepartmentInfo
from flask import jsonify, session, g

'''
def test_read():
    admin_users = db.session.query(User).filter(User.is_admin == 1).all()
    # admin_users = db.session.execute(text('SELECT * FROM users WHERE is_admin = :admin'), {'admin': 1})
    admin_users_dict_list = [user.as_dict() for user in admin_users]

    # 打印结果，供检查
    return admin_users_dict_list
'''

'''
def get_time():
    nowTime = datetime.datetime.now()
    return {
        'Task': 'Connect the frontend and the backend successfully!',
        'Date': nowTime,
        'Frontend': 'React',
        'Backend': 'Flask'
    }
'''


def get_stats():
    admin_num = User.query.filter_by(is_admin=1).count()
    student_num = User.query.filter_by(is_admin=0).count()
    user_num = User.query.count()
    case_num = Case.query.count()
    question_num = TestQuestionPool.query.count()
    exam_num = Exam.query.count()
    return jsonify({
        "adminnum": admin_num,
        "stunum": student_num,
        "usernum": user_num,
        "casenum": case_num,
        "quesnum": question_num,
        "papernum": exam_num,
    })


def user_register(account, password, is_admin, mail, phone):
    if not account:
        return jsonify({'error': '用户名不能为空', 'code': 400}), 400
    if not password:
        return jsonify({'error': '密码不能为空', 'code': 401}), 401
    # if password != confirm_password:
    #     return jsonify({'error': '两次输入的密码不一致', 'code': 402}), 402
    user2 = User.query.all()
    for user1 in user2:
        if user1.account == account:
            return jsonify({'error': '用户名已经存在', 'code': 403}), 403
    if is_admin != 0 and is_admin != 1:
        return jsonify({'error': '需要填写管理员，并且只能是0或1', 'code': 404}), 404
    user3 = User(account=account, password=generate_password_hash(password), is_admin=is_admin, mail=mail, phone=phone)
    db.session.add(user3)
    db.session.commit()
    return jsonify({'message': '注册成功', 'code': 200, 'user': user3.as_dict()}), 200


def user_login(account, password, role):
    user = User.query.filter_by(account=account).first()
    if not account or not password:
        return jsonify({'error': '请输入账号和密码', 'code': 400}), 400
        # 查找用户
    if user and check_password_hash(user.password, password):
        # 验证成功
        token = secrets.token_urlsafe(32)
        session['token'] = token
        session['user_id'] = user.id

        if role == "管理员":
            if user.is_admin == 1:
                message = '登录成功'
            elif user.is_admin == 0:
                message = '权限不匹配'
                return jsonify({'message': message, 'code': 402}), 402
            else:
                message = "权限校验失败，请检查数据库中数据是否正确"
                return jsonify({'message': message, 'user.is_admin': user.is_admin, 'code': 404}), 404
        elif role == "实习生":
            if user.is_admin == 1:
                message = '权限不匹配'
                return jsonify({'message': message, 'code': 402}), 402
            elif user.is_admin == 0:
                message = '登录成功'
            else:
                message = "权限校验失败，请检查数据库中数据是否正确"
                return jsonify({'message': message, 'user.is_admin': user.is_admin, 'code': 404}), 404
        else:
            message = "输入的权限错误"
            return jsonify({'message': message, 'input_role': role, 'code': 403}), 403

        return jsonify({'message': message, 'token': token, 'role': role, 'code': 200}), 200
    else:
        # 验证失败
        return jsonify({'error': '账号或密码错误', 'code': 401}), 401


def user_logout():
    if session:
        session.clear()
    return jsonify({'message': '登出成功', 'code': 200}), 200


def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = user.as_dict()
        if user_dict['is_admin'] == 1:
            role = '管理员'
        elif user_dict['is_admin'] == 0:
            role = '实习生'
        else:
            role = '未知权限'
        user_list.append({'key': user_dict['id'],
                          'name': user_dict['account'],
                          'role': role,
                          'mail': user_dict['mail'],
                          'phone': user_dict['phone']
                          })
    return jsonify({"userlist": user_list, 'code': 200}), 200


def user_update_user(user_id, account, mail, phone, role):
    if not account:
        return jsonify({"message": "修改的用户名不能为空", 'code': 400}), 400
    if not user_id:
        return jsonify({"message": "用户不存在", 'code': 404}), 404
    if role:
        if role == "管理员":
            is_admin = 1
        elif role == "实习生":
            is_admin = 0
        else:
            message = "输入的权限错误"
            return jsonify({'message': message, 'input_role': role, 'code': 403}), 403
    else:
        is_admin = None
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.account = account
        if mail:
            user.mail = mail
        if phone:
            user.phone = phone
        if is_admin:
            user.is_admin = is_admin
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'user': user.as_dict()}), 200
    return jsonify({"message": "用户不存在", 'code': 404}), 404


def change_pwd(user_id, new_pwd):
    if not user_id:
        return jsonify({"message": "id不能为空", 'code': 400}), 400
    if not new_pwd:
        return jsonify({'error': '密码不能为空', 'code': 401}), 401

    user = User.query.filter_by(id=user_id).first()
    if user:
        hashed_password = generate_password_hash(new_pwd)
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200}), 200
    else:
        return jsonify({"message": "用户不存在", 'code': 404}), 404


def admin_delete_user(user_id):
    # 查询并删除用户
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()

        # 获取所有用户
        users = User.query.order_by(User.id).all()
        User.query.delete()
        db.session.commit()  # 确保用户被删除
        # 重置自增主键（这里的 '1' 是新的起始值，根据具体数据库语法可能需要调整）
        db.session.execute(text("ALTER TABLE users AUTO_INCREMENT = 1"))

        # 重新插入用户
        for u in users:
            # 重新创建用户实例并插入
            new_user = User(
                account=u.account,
                password=u.password,
                is_admin=u.is_admin,
                phone=u.phone,
                mail=u.mail
            )
            db.session.add(new_user)

        db.session.commit()
        users = User.query.order_by(User.id).all()
        user_list = []
        for user in users:
            user_dict = user.as_dict()
            if user_dict['is_admin'] == 1:
                role = '管理员'
            elif user_dict['is_admin'] == 0:
                role = '实习生'
            else:
                role = '未知权限'
            user_list.append({'key': user_dict['id'],
                              'name': user_dict['account'],
                              'role': role,
                              'mail': user_dict['mail'],
                              'phone': user_dict['phone']
                              })
        return jsonify({"userlist": user_list, 'code': 200, 'message': "删除成功"}), 200
    else:
        return jsonify({"message": "用户不存在", 'code': 404}), 404


def get_papers():
    exams = Exam.query.order_by(Exam.id.asc()).filter_by(is_delete=0).all()
    exam_num = Exam.query.count()
    return jsonify(
        {"message": "读取成功", 'code': 200, 'length': exam_num, 'exams': [exam.as_dict() for exam in exams]}), 200


def add_paper(key, id, name, time, grade, selected):
    if not key or not id or not name or not time or not grade or not selected:
        return jsonify({"message": "试卷信息不能有空", 'code': 400}), 400
    exam_exists = Exam.query.filter_by(key=key).first()
    if exam_exists:
        return jsonify({'error': '试卷键值已存在，请使用不同的键值', 'code': 401}), 401
    exam_name = Exam.query.filter_by(name=name, is_delete=0).first()
    if exam_name:
        return jsonify({'error': '题目名称被占用，请更换后重试！', 'code': 402}), 402

    new_exam = Exam(key=key, id=id, name=name, time=time, grade=grade, selected=selected)
    db.session.add(new_exam)
    db.session.commit()

    return jsonify({'message': '新增试题成功', 'code': 200, 'exam': new_exam.as_dict()}), 200


def edit_pap(key, id, name, time, grade, selected):
    if not name or not time or not grade or not selected:
        return jsonify({"message": "试卷信息不能有空", 'code': 400}), 400
    exam = Exam.query.filter_by(key=key, id=id, is_delete=0).first()
    if exam:
        exam.name = name
        exam.time = time
        exam.grade = grade
        exam.selected = selected
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'exam': exam.as_dict()}), 200
    else:
        return jsonify({"message": "试卷不存在,或已被删除", 'code': 404}), 404


def delet_paper(key):
    exam = Exam.query.filter_by(key=key, is_delete=0).first()
    if exam:
        exam.is_delete = 1
        db.session.commit()
        exams = Exam.query.filter_by(is_delete=0).all()
        return jsonify({"message": "删除成功", 'code': 200, 'exams': [e.as_dict() for e in exams]}), 200
    else:
        return jsonify({"message": "试卷不存在,或已被删除", 'code': 404}), 404


def get_questions():
    questions = TestQuestionPool.query.order_by(TestQuestionPool.id.asc()).filter_by(is_delete=0).all()
    question_num = TestQuestionPool.query.count()

    return jsonify(
        {"message": "读取成功", 'code': 200, 'length': question_num,
         'questions': [question.as_dict() for question in questions]}), 200


def add_question(key, id, title, A, B, C, D, type, rightchoice):
    if not key or not id or not title or not A or not B or not C or not D or not type or not rightchoice:
        return jsonify({'error': '问题信息不能有空', 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key).first()
    if question_exists:
        return jsonify({'error': '问题键值已存在，请使用不同的键值', 'code': 401}), 401
    question = TestQuestionPool.query.filter_by(title=title, is_delete=0).first()
    if question:
        return jsonify({'error': '问题名称被占用，请更换后重试！', 'code': 402}), 402

    new_question = TestQuestionPool(key=key, id=id, title=title, A=A, B=B, C=C, D=D, type=type, rightchoice=rightchoice)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': '新增问题成功', 'code': 200, 'question': new_question.as_dict()}), 200


def edit_question(key, id, title, A, B, C, D, type, rightchoice):
    if not A or not B or not C or not D or not type or not rightchoice:
        return jsonify({'error': '问题信息不能有空', 'code': 400}), 400
    if not key or not id:
        return jsonify({'error': 'key、id不能有空', 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key, id=id, is_delete=0).first()
    if question_exists:
        question_exists.title = title
        question_exists.A = A
        question_exists.B = B
        question_exists.C = C
        question_exists.D = D
        question_exists.type = type
        question_exists.rightchoice = rightchoice
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'question': question_exists.as_dict()}), 200
    else:
        return jsonify({"message": "问题不存在,或已被删除", 'code': 404}), 404


def delete_question(key):
    exams = Exam.query.filter_by(is_delete=0).all()
    for exam in exams:
        for dict1 in exam.selected:
            if key == dict1['key']:
                return jsonify({"message": "存在与该问题关联的试卷，无法删除", 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key, is_delete=0).first()
    if question_exists:
        question_exists.is_delete = 1
        db.session.commit()
        ques = TestQuestionPool.query.filter_by(is_delete=0).all()
        return jsonify(
            {"message": "删除成功", 'code': 200, 'questions': [q.as_dict() for q in ques]}), 200
    else:
        return jsonify({"message": "问题不存在", 'code': 404}), 404


def user_test(a, key, id):
    exam = Exam.query.filter_by(key=key, id=id, is_delete=0).first()
    list1 = exam.selected
    list2 = []
    for ele in list1:
        key = ele['key']
        Question = TestQuestionPool.query.filter_by(key=key).first()
        question = Question.as_dict()
        question['score'] = ele['score']
        list2.append(question)
    if a == -1:
        return jsonify({"message": "读取试卷成功", 'code': 200, 'exam': list2}), 200
    else:
        exam_key = key
        user_id = g.user.id
        exam_time = exam.time
        new_exam_record = ExamRecord(exam_key=exam_key, user_id=user_id, exam_time=exam_time, score=a)
        db.session.add(new_exam_record)
        db.session.commit()
        return jsonify({"message": "试卷提交成功", 'code': 201, 'exam_record': new_exam_record.as_dict()}), 201


def user_get_test_record():
    exam_records = Exam.query.filter_by(user_id=g.user.id)
    return jsonify({"message": "读取用户记录成功", 'code': 200,
                    'exam_records': [exam_record.as_dict() for exam_record in exam_records]}), 200


def cases_get(del_mes=''):
    cases = Case.query.all()
    if del_mes == '':
        return jsonify(
            {"message": "读取全部病例记录成功", 'code': 200, "cases": [case.as_dict() for case in cases]}), 200
    else:
        return jsonify(
            {"message": "删除成功", 'code': 200, "cases": [case.as_dict() for case in cases]}), 200


def case_get_1(case_type):
    case = Case.query.filter_by(type=case_type)
    list1 = []
    print(case)
    for cas in case:
        list1.append(cas.as_dict())
    return jsonify({"message": "读取病例记录成功", 'code': 200, "cases": list1}), 200


def case_get_2(id):
    case = Case.query.filter_by(id=id).first()
    if not case:
        return jsonify({"message": "病例id不存在", 'code': 400}), 400
    dict1 = case.as_dict()
    case2_0 = Case2.query.filter_by(case_id=id, sign='0').first()
    case2_1 = Case2.query.filter_by(case_id=id, sign='1').first()
    case2_2 = Case2.query.filter_by(case_id=id, sign='2').first()
    dict1['photo_0'] = []
    dict1['photo_1'] = []
    dict1['video'] = []
    if case2_0:
        dict1['photo_0'] = case2_0.media_url
    if case2_1:
        dict1['photo_1'] = case2_1.media_url
    if case2_2:
        dict1['video'] = case2_2.media_url
    return jsonify({"message": "读取病例记录成功", 'code': 200, "case": dict1}), 200


def add_case(name, case_type, admission, examination, diagnosis, treatment_plan, photo_0, photo_1, video):
    if not name or not case_type or not admission or not examination or not diagnosis or not treatment_plan:
        return jsonify({'error': '病例信息不能有空', 'code': 400}), 400
    case = Case.query.filter_by(name=name).first()
    if case:
        return jsonify({'error': '病例名称重复', 'code': 401}), 401
    new_case = Case(
        name=name,
        type=case_type,
        admission=admission,
        examination=examination,
        diagnosis=diagnosis,
        treatment_plan=treatment_plan
    )
    db.session.add(new_case)
    db.session.commit()
    dict1 = new_case.as_dict()
    temp = 0
    if photo_0:
        list1 = []
        for photo in photo_0:
            if photo is None:
                continue
            if photo.get("status", '') != "done":
                head, context = photo['url'].split(",")
                head2, context2 = head.split("/")
                head3, coontext3 = context2.split(";")
                time_str = str(int(datetime.now().timestamp()))
                str1 = str(new_case.id) + "_photo_0_" + str(temp) + time_str + "." + head3
                imgdata = base64.b64decode(context)
                with open("media/" + str1, 'wb') as f:
                    f.write(imgdata)
                temp = temp + 1
                list1.append("http://47.102.142.153:5000/media/" + str1)
        new_case2_0 = Case2(
            case_id=new_case.id,
            media_type='photo',
            media_url=list1,
            sign='0'
        )
        db.session.add(new_case2_0)
        dict1['photo_0'] = new_case2_0.media_url
    else:
        dict1['photo_0'] = []
    temp = 0
    if photo_1:
        list1 = []
        for photo in photo_1:
            if photo is None:
                continue
            if photo.get("status", '') != "done":
                head, context = photo['url'].split(",")
                head2, context2 = head.split("/")
                head3, coontext3 = context2.split(";")
                time_str = str(int(datetime.now().timestamp()))
                str1 = str(new_case.id) + "_photo_1_" + str(temp) + time_str + "." + head3
                imgdata = base64.b64decode(context)
                with open("media/" + str1, 'wb') as f:
                    f.write(imgdata)
                temp = temp + 1
                list1.append("http://47.102.142.153:5000/media/" + str1)
        new_case2_1 = Case2(
            case_id=new_case.id,
            media_type='photo',
            media_url=list1,
            sign='1'
        )
        db.session.add(new_case2_1)
        dict1['photo_1'] = new_case2_1.media_url
        temp = 0
    else:
        dict1['photo_1'] = []
    if video:
        list1 = []
        for photo in video:
            if photo is None:
                continue
            if photo.get("status", '') != "done":
                head, context = photo['url'].split(",")
                head2, context2 = head.split("/")
                head3, coontext3 = context2.split(";")
                time_str = str(int(datetime.now().timestamp()))
                str1 = str(new_case.id) + "_video_" + str(temp) + time_str + "." + head3
                imgdata = base64.b64decode(context)
                with open("media/" + str1, 'wb') as f:
                    f.write(imgdata)
                temp = temp + 1
                list1.append("http://47.102.142.153:5000/media/" + str1)
        new_case2_2 = Case2(
            case_id=new_case.id,
            media_type='video',
            media_url=list1,
            sign='2'
        )
        db.session.add(new_case2_2)
        dict1['video'] = new_case2_2.media_url
    else:
        dict1['video'] = []
    db.session.commit()
    return jsonify({'message': '新增病例成功', 'code': 200, 'case': dict1}), 200


def delete_case(id):
    case = Case.query.filter_by(id=id).first()
    case2s = Case2.query.filter_by(case_id=id)
    if case:
        for case2 in case2s:
            db.session.delete(case2)
        db.session.delete(case)
        db.session.commit()
        return cases_get('删除成功')
    else:
        return jsonify({"message": "病例不存在", 'code': 404}), 404


def edit_case(id, name, case_type, admission, examination, diagnosis, treatment_plan, photo_0, photo_1, video):
    if not name or not case_type or not admission or not examination or not diagnosis or not treatment_plan:
        return jsonify({'error': '病例信息不能有空', 'code': 400}), 400
    case = Case.query.filter_by(id=id).first()
    temp = 0

    if case:
        case.name = name
        case.type = case_type
        case.admission = admission
        case.examination = examination
        case.diagnosis = diagnosis
        case.treatment_plan = treatment_plan
        dict1 = case.as_dict()
        case2_0 = Case2.query.filter_by(case_id=id, sign='0').first()

        if not case2_0:
            list1 = []
            if photo_0:
                for photo in photo_0:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_photo_0_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                new_case2_0 = Case2(
                    case_id=id,
                    media_type='photo',
                    media_url=list1,
                    sign='0'
                )
                db.session.add(new_case2_0)
                dict1['photo_0'] = new_case2_0.media_url
                temp = 0
            else:
                dict1['photo_0'] = []
        else:
            list1 = []
            if photo_0:
                for photo in photo_0:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_photo_0_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                    else:
                        temp = temp + 1
                        list1.append(photo['url'])
                case2_0.media_url = list1
                dict1['photo_0'] = list1
                temp = 0
            else:
                db.session.delete(case2_0)
        case2_1 = Case2.query.filter_by(case_id=id, sign='1').first()
        if not case2_1:
            list1 = []
            if photo_1:
                for photo in photo_1:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_photo_1_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                new_case2_0 = Case2(
                    case_id=id,
                    media_type='photo',
                    media_url=list1,
                    sign='1'
                )
                db.session.add(new_case2_0)
                dict1['photo_1'] = new_case2_0.media_url
                temp = 0
            else:
                dict1['photo_1'] = []
        else:
            list1 = []
            if photo_1:
                for photo in photo_1:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_photo_1_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                    else:
                        temp = temp + 1
                        list1.append(photo['url'])
                case2_1.media_url = list1
                dict1['photo_1'] = case2_1.media_url
                temp = 0
            else:
                db.session.delete(case2_1)
        case2_2 = Case2.query.filter_by(case_id=id, sign='2').first()
        if not case2_2:
            list1 = []
            if video:
                for photo in video:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_video_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                new_case2_0 = Case2(
                    case_id=id,
                    media_type='video',
                    media_url=list1,
                    sign='2'
                )
                db.session.add(new_case2_0)
                dict1['video'] = new_case2_0.media_url
            else:
                dict1['video'] = []
        else:
            list1 = []
            if video:
                for photo in video:
                    if photo is None:
                        continue
                    if photo.get("status", '') != "done":
                        head, context = photo['url'].split(",")
                        head2, context2 = head.split("/")
                        head3, coontext3 = context2.split(";")
                        time_str = str(int(datetime.now().timestamp()))
                        str1 = str(id) + "_video_" + str(temp) + time_str + "." + head3
                        imgdata = base64.b64decode(context)
                        with open("media/" + str1, 'wb') as f:
                            f.write(imgdata)
                        temp = temp + 1
                        list1.append("http://47.102.142.153:5000/media/" + str1)
                    else:
                        temp = temp + 1
                        list1.append(photo['url'])
                case2_2.media_url = list1
                dict1['video'] = case2_2.media_url
            else:
                db.session.delete(case2_2)
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'case': dict1}), 200
    else:
        return jsonify({"message": "病例不存在", 'code': 404}), 404


def fee_get():
    projects = FeeItem.query.all()
    p_list = [project.as_dict() for project in projects]
    for i in p_list:
        i['key'] = i.pop('id')
    return jsonify(
        {"message": "读取成功", 'code': 200, 'projectlist': p_list}), 200


def fee_add(key, name, type, description, img, price):
    if not key or not name or not type or not description or not img or not price:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    fee = FeeItem.query.filter_by(id=key).first()
    if fee:
        return jsonify({'error': '键值已经存在', 'code': 401}), 401
    head, context = img.split(",")
    head2, context2 = head.split("/")
    head3, coontext3 = context2.split(";")
    time_str = str(int(datetime.now().timestamp()))
    str1 = str(key) + "_fee_" + time_str + "." + head3
    imgdata = base64.b64decode(context)
    with open("media/" + str1, 'wb') as f:
        f.write(imgdata)
    str2 = "http://47.102.142.153:5000/media/" + str1
    new_fee = FeeItem(
        id=key,
        name=name,
        type=type,
        description=description,
        img=str2,
        price=price
    )
    db.session.add(new_fee)
    db.session.commit()
    return jsonify({'message': '新增收费项目成功', 'code': 200, 'case': new_fee.as_dict()}), 200


def fee_delete(id):
    fee = FeeItem.query.filter_by(id=id).first()
    if fee:
        db.session.delete(fee)
        db.session.commit()
        # 获取所有用户
        fees = FeeItem.query.order_by(FeeItem.id).all()
        FeeItem.query.delete()
        db.session.commit()  # 确保用户被删除
        # 重置自增主键（这里的 '1' 是新的起始值，根据具体数据库语法可能需要调整）
        db.session.execute(text("ALTER TABLE fee_item AUTO_INCREMENT = 1"))

        # 重新插入用户
        for f in fees:
            # 重新创建用户实例并插入
            print('last:', f.as_dict())
            new_f = FeeItem(
                name=f.name,
                type=f.type,
                price=f.price,
                description=f.description,
                img=f.img,
                update_time=f.update_time
            )
            print('new:', new_f.as_dict())
            db.session.add(new_f)
        db.session.commit()
        fees = FeeItem.query.order_by(FeeItem.id).all()
        f_list = [f.as_dict() for f in fees]
        for i in f_list:
            i['key'] = i.pop('id')
        return jsonify({"feelist": f_list, 'code': 200, 'message': "删除成功"}), 200
    else:
        return jsonify({"message": "收费项目不存在", 'code': 404}), 404


def fee_edit(key, name, type, description, img, price):
    if not key or not name or not type or not description or not img or not price:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    fee = FeeItem.query.filter_by(id=key).first()
    if img != 'done':
        head, context = img.split(",")
        head2, context2 = head.split("/")
        head3, coontext3 = context2.split(";")
        time_str = str(int(datetime.now().timestamp()))
        str1 = str(key) + "_fee_" + time_str + "." + head3
        imgdata = base64.b64decode(context)
        with open("media/" + str1, 'wb') as f:
            f.write(imgdata)
        new_img = "http://47.102.142.153:5000/media/" + str1
    else:
        new_img = '' if not fee else fee.img
    if fee:
        fee.name = name
        fee.type = type
        fee.description = description
        fee.img = new_img
        fee.price = price
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'case': fee.as_dict()}), 200
    else:
        return jsonify({"message": "收费项目不存在", 'code': 404}), 404


def department_get():
    departments = DepartmentInfo.query.all()
    return jsonify({"message": "读取科室信息成功", 'code': 200,
                    "departments": [department.as_dict() for department in departments]}), 200


def department_edit(key, name, department_info, picture, video):
    if not key or not name or not department_info:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    department = DepartmentInfo.query.filter_by(id=key).first()
    list1 = []
    temp = 0
    if picture != []:
        for photo in picture:
            if photo.get("status", '') != "done":
                head, context = photo['url'].split(",")
                head2, context2 = head.split("/")
                head3, coontext3 = context2.split(";")
                time_str = str(int(datetime.now().timestamp()))
                str1 = str(key) + "_dep_picture" + str(temp) + time_str + "." + head3
                imgdata = base64.b64decode(context)
                with open("media/" + str1, 'wb') as f:
                    f.write(imgdata)
                temp = temp + 1
                list1.append("http://47.102.142.153:5000/media/" + str1)
            else:
                temp = temp + 1
                list1.append(photo['url'])
    list2 = []
    temp = 0
    if video != []:
        for video1 in video:
            if video1.get("status") != "done":
                head, context = video1['url'].split(",")
                head2, context2 = head.split("/")
                head3, coontext3 = context2.split(";")
                time_str = str(int(datetime.now().timestamp()))
                str1 = str(key) + "_dep_video" + str(temp) + time_str + "." + head3
                imgdata = base64.b64decode(context)
                with open("media/" + str1, 'wb') as f:
                    f.write(imgdata)
                temp = temp + 1
                list2.append("http://47.102.142.153:5000/media/" + str1)
            else:
                temp = temp + 1
                list2.append(video1['url'])
    if department:
        department.name = name
        department.department_info = department_info
        department.picture = list1
        department.video = list2
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'case': department.as_dict()}), 200
    else:
        return jsonify({"message": "科室不存在", 'code': 404}), 404


def case3_add(key, name, phone, age, gender, file):
    if not key or not name or not phone or not age or not gender or not file:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    case = Case3.query.filter_by(id=key)
    if case:
        return jsonify({'error': '键值已经存在', 'code': 401}), 401
    new_case = Case3(
        id=key,
        name=name,
        phone=phone,
        age=age,
        gender=gender,
        file=file
    )
    db.session.add(new_case)
    db.session.commit()
    return jsonify({'message': '新增人员病例档案成功', 'code': 200, 'case': new_case.as_dict()}), 200


def case3_get(del_mes=''):
    projects = Case3.query.all()
    if del_mes == '':
        return jsonify(
            {"message": "读取成功", 'code': 200, 'Caselist': [project.as_dict() for project in projects]}), 200
    else:
        return jsonify(
            {"message": "删除成功", 'code': 200, 'Caselist': [project.as_dict() for project in projects]}), 201


def case3_delete(id):
    case = Case3.query.filter_by(id=id).first()
    if case:
        db.session.delete(case)
        db.session.commit()
        return case3_get('删除成功')
    else:
        return jsonify({"message": "人员病例档案不存在", 'code': 404}), 404


def case3_edit(key, name, phone, age, gender, file):
    if not key or not name or not phone or not age or not gender or not file:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    case3 = Case3.query.filter_by(id=key).first()
    if case3:
        case3.name = name
        case3.type = phone
        case3.description = age
        case3.img = gender
        case3.price = file
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'case': case3.as_dict()}), 200
    else:
        return jsonify({"message": "人员病例不存在", 'code': 404}), 404


def get_assist(message):
    if not message:
        return jsonify({'error': '信息不能有空', 'code': 400}), 400
    query = message[-1].get("content")
    history = []
    for i in range(len(message)-1):
        history.append(message[i])
    # 使用模型进行处理
    url = 'https://u384232-8174-307abb43.westc.gpuhub.com:8443/chat/knowledge_base_chat'
    print(history)
    transhistory = [
        {"role": item["role"], "content": item["content"]} for item in history if item["role"] != "assistant"
    ]
    print(json.dumps(transhistory, ensure_ascii=False, indent=4))
    data = {
        "query": query,
        "knowledge_base_name": "samples",
        "top_k": 5,
        "score_threshold": 1,
        "history": transhistory,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "default"
    }
    # Convert data to JSON string
    response = requests.post(url, data=json.dumps(data))
    data=response.json()
    value1 = data["answer"]
    print(value1)
    return jsonify({"message": value1, 'code': 200}), 200