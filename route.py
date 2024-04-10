from flask import request

from function import user_login, user_register, get_stats, user_logout, get_users, user_update_user, user_change_pwd, admin_delete_user, \
    get_papers, add_paper,edit_pap,delet_paper,get_questions,add_question,edit_question,delete_question, admin_update_user, admin_change_pwd,\
    user_test,user_get_test_record,cases_get,case_get_1,case_get_2,add_case,edit_case,delete_case

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

    @app.route('/admin', methods=['GET'])
    def get_stat():
        return get_stats()

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        account = data.get('account')
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        is_admin = data.get("is_admin")
        return user_register(account, password, confirm_password, is_admin)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        account = data.get('account')
        password = data.get('password')
        return user_login(account, password)

    @app.route('/user/logout', methods=['POST'])
    def logout():
        return user_logout()

    @app.route('/getuser', methods=['GET'])
    def get_user():
        return get_users()

    @app.route('/user/update_user_info', methods=['POST'])
    def update_user_info():
        data = request.json
        name = data.get('account')
        return user_update_user(name)

    @app.route('/user/change_password', methods=['POST'])
    def change_password():
        data = request.json
        new_password = data.get('pwd')
        confirm_password = data.get('confirm_pwd')
        return user_change_pwd(new_password,confirm_password)

    @app.route('/admin/update_user_info/<id>', methods=['POST'])
    def admin_update_user_info(id):
        data = request.json
        id = id
        name = data.get('account')
        return admin_update_user(id,name)

    @app.route('/admin/change_password/<id>', methods=['POST'])
    def admin_change_password(id):
        data = request.json
        id = id
        new_password = data.get('pwd')
        confirm_password = data.get('confirm_pwd')
        return admin_change_pwd(id,new_password,confirm_password)

    @app.route('/admin/delete_user/<id>', methods=['POST'])
    def del_user(id):
        id = id
        return admin_delete_user(id)

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

    @app.route('/admin/test-paper/edit/<key>/<id>', methods=['POST'])
    def edit_test_paper(key,id):
        data = request.json
        edit_paper = edit_pap(key,
                              id,
                              data['name'],
                              data['time'],
                              data['grade'],
                              data['selected'])
        return edit_paper

    @app.route('/admin/test-paper/delete/<key>/<id>', methods=['post'])
    def delete_test_paper(key,id):
        return delet_paper(key,id)

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

    @app.route('/admin/question/edit/<key>/<id>/<title>', methods=['POST'])
    def edit_test_question(key,id,title):
        data = request.json
        edited_question = edit_question(key,
                                        id,
                                        title,
                                        data['A'],
                                        data['B'],
                                        data['C'],
                                        data['D'],
                                        data['type'],
                                        data['rightchoice'])
        return edited_question

    @app.route('/admin/question/delete/<key>/<id>/<title>', methods=['POST'])
    def delete_test_question(key,id,title):
        return delete_question(key, id,title)

    @app.route('/user/test/<key>/<id>', methods=['GET','POST'])
    def test(key,id):
        a=0
        if request.method == 'GET':
            return user_test(a,key,id)
        else:
            score=request.json.get("score")
            return user_test(score,key,id)

    @app.route('/user/test_record', methods=['GET'])
    def test_record():
        return user_get_test_record()



    @app.route('/case/get', methods=['GET'])
    def get_cases():
        return cases_get()

    @app.route('/case/get/<name>', methods=['GET'])
    def get_case(name):
        return case_get_1(name)

    @app.route('/case/get/<id>', methods=['GET'])
    def get_case_2(id):
        return case_get_1(id)

    @app.route('/admin/case/add', methods=['POST'])
    def add_cases():
        data = request.json
        new_case = add_case(
            data['name'],
            data['admission'],
            data['examination'],
            data['diagnosis'],
            data['treatment_plan']
        )
        return new_case

    @app.route('/admin/case/edit/<id>', methods=['POST'])
    def edit_cases(id):
        data = request.json
        edit_case1 = edit_case(id,
            data['name'],
            data['admission'],
            data['examination'],
            data['diagnosis'],
            data['treatment_plan']
        )
        return edit_case1

    @app.route('/admin/case/delete/<id>', methods=['post'])
    def delete_cases(id):
        return delete_case(id)