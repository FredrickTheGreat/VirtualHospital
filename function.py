import json
import secrets
from db_init import db, app
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Case, TestQuestionPool, Exam, ExamRecord, Case2
from flask import jsonify, session, g
from flask import request
import requests

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


def user_register(account, password, confirm_password, is_admin, mail, phone):
    if not account:
        return jsonify({'error': '用户名不能为空', 'code': 400}), 400
    if not password or not confirm_password:
        return jsonify({'error': '密码不能为空', 'code': 401}), 401
    if password != confirm_password:
        return jsonify({'error': '两次输入的密码不一致', 'code': 402}), 402
    user2 = User.query.all()
    for user1 in user2:
        if user1.account == account:
            return jsonify({'error': '用户名已经存在', 'code': 403}), 403
    if is_admin != 0 and is_admin != 1:
        return jsonify({'error': '需要填写管理员，并且只能是0或1', 'code': 404}), 404
    user3 = User(account=account, password=generate_password_hash(password), is_admin=is_admin, mail=mail, phone=phone)
    db.session.add(user3)
    db.session.commit()
    return jsonify({'message': '注册成功', 'user': user3.as_dict()}), 200


def user_login(account, password):
    user = User.query.filter_by(account=account).first()
    if not account or not password:
        return jsonify({'error': '请输入账号和密码', 'code': 400}), 400
        # 查找用户
    if user and check_password_hash(user.password, password):
        # 验证成功
        token = secrets.token_urlsafe(32)
        session['token'] = token
        session['user_id'] = user.id
        return jsonify({'message': '登录成功', 'user': user.as_dict(), 'token': token, 'code': 200}), 200
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
        else:
            role = '实习生'
        user_list.append({'key': user_dict['id'],
                          'name': user_dict['account'],
                          'role': role,
                          'mail': user_dict['mail'],
                          'phone': user_dict['phone']
                          })
    return jsonify({"userlist": user_list, 'code': 200}), 200


def user_update_user(account, mail, phone):
    if not account:
        return jsonify({"message": "修改的用户名不能为空", 'code': 400}), 400
    user = User.query.filter_by(id=g.user.id).first()
    if user:
        user.account = account
        if mail:
            user.mail = mail
        if phone:
            user.phone = phone
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'user': user.as_dict()}), 200
    return jsonify({"message": "用户不存在", 'code': 404}), 404


def user_change_pwd(new_pwd, confirm_password):
    if not new_pwd or not confirm_password:
        return jsonify({'error': '密码不能为空', 'code': 401}), 401
    if new_pwd != confirm_password:
        return jsonify({'error': '两次输入的密码不一致', 'code': 402}), 402

    if g and g.get("user") and g.get("user").id:
        user = User.query.filter_by(id=g.user.id).first()
        hashed_password = generate_password_hash(new_pwd)
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200}), 200
    else:
        return jsonify({"message": "用户不存在", 'code': 404}), 404


def admin_update_user(id, account, mail, phone):
    if not account or not id:
        return jsonify({"message": "id和要修改的信息不能为空", 'code': 400}), 400
    user = User.query.filter_by(id=id).first()
    if user:
        user.account = account
        if mail:
            user.mail = mail
        if phone:
            user.phone = phone
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'user': user.as_dict()}), 200
    return jsonify({"message": "用户不存在", 'code': 404}), 404


def admin_change_pwd(id, new_pwd, confirm_password):
    if not id:
        return jsonify({"message": "id不能为空", 'code': 400}), 400
    if not (new_pwd or confirm_password):
        return jsonify({'error': '密码不能为空', 'code': 401}), 401
    if new_pwd != confirm_password:
        return jsonify({'error': '两次输入的密码不一致', 'code': 402}), 402
    user = User.query.filter_by(id=id).first()
    if user:
        hashed_password = generate_password_hash(new_pwd)
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200}), 200
    else:
        return jsonify({"message": "用户不存在", 'code': 404}), 404


def admin_delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user_dict = user.as_dict()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"userlist": user_dict, 'code': 200, 'message': "删除成功"}), 200
    else:
        return jsonify({"message": "用户不存在", 'code': 404}), 404


def get_papers():
    exams = Exam.query.order_by(Exam.id.asc()).filter_by(is_delete=0).all()

    return jsonify({"message": "读取成功", 'code': 200, 'exams': [exam.as_dict() for exam in exams]}), 200


def add_paper(key, id, name, time, grade, selected):
    if not key or not id or not name or not time or not grade or not selected:
        return jsonify({"message": "试卷信息不能有空", 'code': 400}), 400
    exam_exists = Exam.query.filter_by(key=key, id=id).first()
    if exam_exists:
        return jsonify({'error': '试卷键值已存在，请使用不同的键值', 'code': 401}), 401
    exam = Exam.query.filter_by(name=name).first()
    if exam:
        return jsonify({'error': '题目名称被占用，请更换后重试！', 'code': 402}), 402
    new_exam = Exam(key=key, id=id, name=name, time=time, grade=grade, selected=selected)
    db.session.add(new_exam)
    db.session.commit()

    return jsonify({'message': '新增试题成功', 'code': 200, 'exam': new_exam.as_dict()}), 200


def edit_pap(key, id, name, time, grade, selected):
    if not name or not time or not grade or not selected:
        return jsonify({"message": "试卷信息不能有空", 'code': 400}), 400
    exam = Exam.query.filter_by(key=key, id=id).first()
    if exam:
        exam.name = name
        exam.time = time
        exam.grade = grade
        exam.selected = selected
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'exam': exam.as_dict()}), 200
    else:
        return jsonify({"message": "试卷不存在", 'code': 404}), 404


def delet_paper(key, id):
    exam = Exam.query.filter_by(key=key, id=id).first()
    if exam:
        exam.is_delete = 1
        exam_dict = exam.as_dict()
        db.session.commit()
        return jsonify({"message": "删除成功", 'code': 201, 'exams': exam_dict}), 201
    else:
        return jsonify({"message": "试卷不存在", 'code': 404}), 404


def get_questions():
    questions = TestQuestionPool.query.order_by(TestQuestionPool.id.asc()).all()

    return jsonify(
        {"message": "读取成功", 'code': 200, 'questions': [question.as_dict() for question in questions]}), 200


def add_question(key, id, title, A, B, C, D, type, rightchoice):
    if not key or not id or not title or not A or not B or not C or not D or not type or not rightchoice:
        return jsonify({'error': '问题信息不能有空', 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key, id=id, title=title).first()
    if question_exists:
        return jsonify({'error': '问题键值已存在，请使用不同的键值', 'code': 401}), 401
    question = TestQuestionPool.query.filter_by(title=title).first()
    if question:
        return jsonify({'error': '问题名称被占用，请更换后重试！', 'code': 402}), 402

    new_question = TestQuestionPool(key=key, id=id, title=title, A=A, B=B, C=C, D=D, type=type, rightchoice=rightchoice)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': '新增问题成功', 'code': 200, 'question': new_question.as_dict()}), 200


def edit_question(key, id, title, A, B, C, D, type, rightchoice):
    if not A or not B or not C or not D or not type or not rightchoice:
        return jsonify({'error': '问题信息不能有空', 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key, id=id, title=title).first()
    if question_exists:
        question_exists.A = A
        question_exists.B = B
        question_exists.C = C
        question_exists.D = D
        question_exists.type = type
        question_exists.rightchoice = rightchoice
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'exam': question_exists.as_dict()}), 200
    else:
        return jsonify({"message": "问题不存在", 'code': 404}), 404


def delete_question(key, id, title):
    exams = Exam.query.filter_by(is_delete=0).all()
    for exam in exams:
        for dict1 in exam.selected:
            if key == dict1['key']:
                return jsonify({"message": "存在与该问题关联的试卷，无法删除", 'code': 400}), 400
    question_exists = TestQuestionPool.query.filter_by(key=key, id=id, title=title).first()
    if question_exists:
        qus_dict = question_exists.as_dict()
        db.session.delete(question_exists)
        db.session.commit()
        return jsonify(
            {"message": "删除成功", 'code': 201, 'questions': qus_dict}), 201
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
    if a == 0:
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


def cases_get():
    cases = Case.query.all()
    return jsonify({"message": "读取全部病例记录成功", 'code': 200, "cases": [case.as_dict() for case in cases]}), 200


def case_get_1(name):
    case = Case.query.filter_by(name=name).first()
    return jsonify({"message": "读取病例记录成功", 'code': 200, "case": case.as_dict()}), 200


def case_get_2(id):
    case = Case.query.filter_by(id=id).first()
    dict1 = case.as_dict()
    case2s = Case2.query.filter_by(case_id=id)
    list1 = []
    for case2 in case2s:
        dict2 = case2.as_dict()
        dict3 = {dict2['media_type']: dict2['media_url']}
        list1.append(dict3)
    dict1['media_list'] = list1
    return jsonify({"message": "读取病例记录成功", 'code': 200, "case": dict1}), 200


def add_case(name, admission, examination, diagnosis, treatment_plan):
    if not name or not admission or not examination or not diagnosis or not treatment_plan:
        return jsonify({'error': '病例信息不能有空', 'code': 400}), 400
    case = Case.query.filter_by(name=name)
    if case:
        return jsonify({'error': '病例名称重复', 'code': 401}), 401
    new_case = Case(
        name=name,
        admission=admission,
        examination=examination,
        diagnosis=diagnosis,
        treatment_plan=treatment_plan
    )
    db.session.add(new_case)
    db.session.commit()
    return jsonify({'message': '新增病例成功', 'code': 200, 'case': new_case.as_dict()}), 200


def delete_case(id):
    case = Case.query.filter_by(id=id).first()
    if case:
        case_dict = case.as_dict()
        db.session.delete(case)
        db.session.commit()
        return jsonify(
            {"message": "删除成功", 'code': 201, 'case': case_dict}), 201
    else:
        return jsonify({"message": "病例不存在", 'code': 404}), 404


def edit_case(id, name, admission, examination, diagnosis, treatment_plan):
    if not name or not admission or not examination or not diagnosis or not treatment_plan:
        return jsonify({'error': '病例信息不能有空', 'code': 400}), 400
    case = Case.query.filter_by(id=id).first()
    if case:
        case.name = name
        case.admission = admission
        case.examination = examination
        case.diagnosis = diagnosis
        case.treatment_plan = treatment_plan
        db.session.commit()
        return jsonify({"message": "修改成功", 'code': 200, 'case': case.as_dict()}), 200
    else:
        return jsonify({"message": "病例不存在", 'code': 404}), 404


def get_assist(query,id):
    # 使用模型进行处理
    url = 'https://u384232-8174-307abb43.westc.gpuhub.com:8443/chat/knowledge_base_chat'
    data = {
        "ChatId":id,
        "query": query,
        "knowledge_base_name": "virtualHospital",
        "top_k": 5,
        "score_threshold": 1,
        "history": [
            {
                "role": "user",
                "content": "我们来玩成语接龙，我先来，生龙活虎"
            },
            {
                "role": "assistant",
                "content": "虎头虎脑"
            }
        ],
        "stream": False,
        "local_doc_url": False
    }
    # Convert data to JSON string
    response = requests.post(url, data=json.dumps(data))
    response = response.json()
    value1 = response['answer']
    print(value1)
    return jsonify({"message": value1, 'code': 200}), 200