from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(255), nullable=False, comment='账户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    is_admin = db.Column(db.Integer, nullable=False, comment='enum(0,1)(0-用户,1-管理员)')
    phone = db.Column(db.String(20), nullable=True)
    mail = db.Column(db.String(127), nullable=True)

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    admission = db.Column(db.Text)
    examination = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    # 关系定义，'lazy' 定义了如何加载相关对象
    case_studies = db.relationship('Case2', backref='case', lazy=True)

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Case2(db.Model):
    __tablename__ = 'case2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    media_type = db.Column(db.Enum('photo', 'video'), nullable=False)
    media_url = db.Column(db.JSON, nullable=False)
    sign = db.Column(db.Enum('0', '1', '2'), nullable=False)

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DepartmentInfo(db.Model):
    __tablename__ = 'department_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='科室id')
    name = db.Column(db.String(255), nullable=False, comment='科室名称')
    can_view = db.Column(db.Integer, default=1, nullable=False, comment='是否可以被访问（1 可以 0 不行）',
                         info={'invisible': True})
    picture = db.Column(db.JSON, nullable=False, comment='科室图片')
    department_info = db.Column(db.String(1023), nullable=True, comment='科室介绍')
    video = db.Column(db.JSON, nullable=False, comment='科室视频')

    __table_args__ = (
        db.UniqueConstraint('id', name='department_information_pk_2'),
        {'comment': '科室信息表'},
    )

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Case3(db.Model):
    __tablename__ = 'case3'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, nullable=False, comment='就诊人id')
    file = db.Column(db.String(255), nullable=False, comment='文件存储路径')
    update_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now, comment='更新时间')
    phone = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('id', name='case_pk'),
        {'comment': '病例档案'},
    )

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Exam(db.Model):
    __tablename__ = 'exam'

    key = db.Column(db.String(255), primary_key=True, nullable=False)
    id = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.String(255), nullable=False)
    selected = db.Column(db.JSON, nullable=False)
    is_delete = db.Column(db.Integer, default=0, nullable=False, comment='(0为在使用， 1为已删除)')

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ExamRecord(db.Model):
    __tablename__ = 'exam_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_key = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    exam_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    score = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class FeeItem(db.Model):
    __tablename__ = 'fee_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, comment='收费项目类型')
    price = db.Column(db.Integer, nullable=True, comment='价格')
    description = db.Column(db.String(1023), nullable=True, comment='收费项目介绍')
    img = db.Column(db.String(255), nullable=True, comment='图片所在地址')
    update_time = db.Column(db.TIMESTAMP, nullable=True, comment='更新时间',default=datetime.now())
    name = db.Column(db.String(255), nullable=True, comment="收费项目名称")

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TestQuestionPool(db.Model):
    __tablename__ = 'test_question_pool'

    key = db.Column(db.String(255), primary_key=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), primary_key=True, nullable=False)
    A = db.Column(db.Text, nullable=False)
    B = db.Column(db.Text, nullable=False)
    C = db.Column(db.Text, nullable=False)
    D = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    rightchoice = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Integer, default=0, nullable=False, comment='(0为在使用， 1为已删除)')

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Visitor(db.Model):
    __tablename__ = 'visitor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='就诊人唯一id')
    master_name = db.Column(db.String(255), nullable=False, comment='宠物所有人name')
    pet_type = db.Column(db.String(255), nullable=False, comment='宠物物种')
    pet_name = db.Column(db.Integer, nullable=False)
    pet_sex = db.Column(db.Integer, nullable=False, comment='宠物性别（0母1公）')
    registration_time = db.Column(db.TIMESTAMP, nullable=False, comment='注册时间（第一次来的时间）')
    last_visit_time = db.Column(db.TIMESTAMP, nullable=False, comment='最近一次就诊时间')
    pet_age = db.Column(db.Integer, nullable=True)
    tel = db.Column(db.String(20), nullable=True)

    def as_dict(self):
        """将对象转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
