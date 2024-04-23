import os

from flask import request, send_from_directory

from function import user_login, user_register, get_stats, user_logout, get_users, user_update_user, \
    admin_delete_user, \
    get_papers, add_paper, edit_pap, delet_paper, get_questions, add_question, edit_question, delete_question, \
    user_test, user_get_test_record, cases_get, case_get_1, case_get_2, add_case, edit_case, delete_case, change_pwd, \
    fee_get, fee_add, fee_edit, fee_delete, department_edit, department_get, case3_add, case3_delete, case3_get, \
    get_assist


def init_routes(app):
    '''
    @app.route('/time', methods=['POST'])
    def get_time_route():
        data = request.json.get('test')
        ret = get_time()
        ret['test'] = data+10 if data else 1
        return ret

    @app.route('/user', methods=['GET'])
    def test_read_route():
        ret = test_read()
        return ret
    '''

    @app.route('/media/<file_path>')
    def get_media(file_path):
        return send_from_directory(os.path.join(app.root_path, 'media'), file_path)

    @app.route('/admin', methods=['GET'])
    def get_stat():
        return get_stats()

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        account = data.get('account')
        password = data.get("password")
        is_admin = data.get("is_admin")
        mail = data.get("mail")
        phone_num = data.get("phone")
        return user_register(account, password, is_admin, mail, phone_num)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        account = data.get('account')
        password = data.get('password')
        role = data.get('role')
        return user_login(account, password, role)

    @app.route('/user/logout', methods=['POST'])
    def logout():
        return user_logout()

    @app.route('/getuser', methods=['GET'])
    def get_user():
        return get_users()

    @app.route('/update_user_info', methods=['POST'])
    def update_user_info():
        data = request.json
        user_id = data.get('id')
        name = data.get('account')
        mail = data.get('mail')
        phone = data.get('phone')
        role = data.get('role')
        return user_update_user(user_id, name, mail, phone, role)

    @app.route('/admin/change_password', methods=['POST'])
    def change_password():
        data = request.json
        user_id = data.get('id')
        new_password = data.get('pwd')
        return change_pwd(user_id, new_password)

    @app.route('/admin/delete_user', methods=['POST'])
    def del_user():
        data = request.json
        user_id = data.get('id')
        return admin_delete_user(user_id)

    @app.route('/test-paper/get', methods=['GET'])
    def get_test_papers():
        return get_papers()

    @app.route('/admin/test-paper/add', methods=['POST'])
    def add_test_paper():
        data = request.json
        new_paper = add_paper(data['key'],
                              data['id'],
                              data['name'],
                              data['time'],
                              data['grade'],
                              data['selected'])
        return new_paper

    @app.route('/admin/test-paper/edit', methods=['POST'])
    def edit_test_paper():
        data = request.json
        key = data.get("key")
        id = data.get("id")
        name = data.get("name")
        time = data.get("time")
        grade = data.get("grade")
        selected = data.get("selected")
        edit_paper = edit_pap(key, id, name, time, grade, selected)
        return edit_paper

    @app.route('/admin/test-paper/delete/<key>', methods=['GET'])
    def delete_test_paper(key):
        return delet_paper(key)

    @app.route('/question/get', methods=['GET'])
    def get_test_questions():
        return get_questions()

    @app.route('/admin/question/add', methods=['POST'])
    def add_test_question():
        data = request.json
        new_question = add_question(data['key'],
                                    data['id'],
                                    data['title'],
                                    data['A'],
                                    data['B'],
                                    data['C'],
                                    data['D'],
                                    data['type'],
                                    data['rightchoice'])
        return new_question

    @app.route('/admin/question/edit', methods=['POST'])
    def edit_test_question():
        data = request.json
        key = data.get("key")
        id = data.get("id")
        A = data.get("A")
        B = data.get("B")
        C = data.get("C")
        D = data.get("D")
        type = data.get("type")
        rightchoice = data.get("rightchoice")
        title = data.get("title")
        edited_question = edit_question(key, id, title, A, B, C, D, type, rightchoice)
        return edited_question

    @app.route('/admin/question/delete/<key>', methods=['GET'])
    def delete_test_question(key):
        return delete_question(key)

    @app.route('/user/test/<key>/<id>', methods=['GET', 'POST'])
    def test(key, id):
        a = -1
        if request.method == 'GET':
            return user_test(a, key, id)
        else:
            score = request.json.get("score")
            return user_test(score, key, id)

    @app.route('/user/test_record', methods=['GET'])
    def test_record():
        return user_get_test_record()

    @app.route('/case/get', methods=['GET'])
    def get_cases():
        return cases_get()

    @app.route('/case/get/type=<case_type>', methods=['GET'])
    def get_case(case_type):
        return case_get_1(case_type)

    @app.route('/case/get/id=<id>', methods=['GET'])
    def get_case_2(id):
        return case_get_2(id)

    @app.route('/admin/case/add', methods=['POST'])
    def add_test_case():
        data = request.json
        name = data.get("name")
        type = data.get("type")
        admission = data.get("admission")
        examination = data.get("examination")
        diagnosis = data.get("diagnosis")
        treatment_plan = data.get("treatment_plan")
        photo_0 = request.json.get("photo_0")
        photo_1 = data.get("photo_1")
        video = data.get("video")
        new_case = add_case(
            name,
            type,
            admission,
            examination,
            diagnosis,
            treatment_plan,
            photo_0,
            photo_1,
            video
        )
        return new_case

    @app.route('/admin/case/edit/<id>', methods=['POST'])
    def edit_test_case(id):
        data = request.json
        edit_case1 = edit_case(id,
                               data['name'],
                               data['type'],
                               data['admission'],
                               data['examination'],
                               data['diagnosis'],
                               data['treatment_plan'],
                               data['photo_0'],
                               data['photo_1'],
                               data['video']
                               )
        return edit_case1

    @app.route('/admin/case/delete/<id>', methods=['post'])
    def delete_test_case(id):
        return delete_case(id)

    @app.route('/fee/get', methods=['GET'])
    def get_fee():
        return fee_get()

    @app.route('/admin/fee/add', methods=['POST'])
    def add_fee():
        data = request.json
        new_fee = fee_add(
            data.get('key'),
            data.get('name'),
            data.get('type'),
            data.get('description'),
            data.get('img'),
            data.get('price')
        )
        return new_fee

    @app.route('/admin/fee/edit/<key>', methods=['POST'])
    def edit_fee(key):
        data = request.json
        edit_fee1 = fee_edit(key,
                             data['name'],
                             data['type'],
                             data['description'],
                             data['img'],
                             data['price']
                             )
        return edit_fee1

    @app.route('/admin/fee/delete/<id>', methods=['post'])
    def delete_fee(id):
        return fee_delete(id)

    @app.route('/department/get', methods=['GET'])
    def get_department():
        return department_get()

    @app.route('/admin/department/edit/<key>', methods=['POST'])
    def edit_department(key):
        data = request.json
        edit_department1 = department_edit(key,
                                           data['name'],
                                           data['department_info'],
                                           data['picture'],
                                           data['video']
                                           )
        return edit_department1

    @app.route('/admin/case3/get', methods=['GET'])
    def get_case3():
        return case3_get()

    @app.route('/admin/case3/add', methods=['POST'])
    def add_case3():
        data = request.json
        new_case3 = case3_add(
            data['key'],
            data['name'],
            data['phone'],
            data['age'],
            data['gender'],
            data['file']
        )
        return new_case3

    @app.route('/admin/case3/edit/<key>', methods=['POST'])
    def edit_case3(key):
        data = request.json
        edit_case3 = fee_edit(key,
                              data['name'],
                              data['phone'],
                              data['age'],
                              data['gender'],
                              data['file']
                              )
        return edit_case3

    @app.route('/admin/case3/delete/<id>', methods=['post'])
    def delete_case3(id):
        return case3_delete(id)

    @app.route('/assist', methods=['post'])
    def assist():
        # 获取 JSON 请求体中的数据
        data = request.json
        messages = data.get("messages")
        # print(data)
        return get_assist(messages)
