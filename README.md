
# Python Flask+SQLAlchemy后端项目安装步骤
## 代码仓库地址：https://github.com/FredrickTheGreat/VirtualHospital
## 软件需求：
Python: 3.10,官网下载
PyCharm：2022.2.4，官网下载
DataGrip：2023.3.4，官网下载
Postman: 9.14.0，官网下载
数据库: MySQL 8.0，官网下载

## 依赖安装：
pip install flask
pip install sqlalchemy 
pip install flask_sqlalchemy
pip install pymysql

## 配置数据库：
通过MySQL的账号密码配置数据库,配置好后在setting.py里修改
# 数据库信息
HOSTNAME = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'rfy6662949'
DATABASE = 'my_db_01'
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI
SECRET_KEY = "KSOA;DKSAOP,;PSA"

## 配置本地连接：
通过本地端口和flask内置服务器测试
在服务器上运行app.py启动项目
配置服务器连接：
使用阿里云的服务器，在安全组设置中公开5000端口

## 问题处理
数据库问题：
确保MySQL组件安装齐全。
确保数据库服务正在运行。
确保数据库用户名、密码及权限设置是否正确。

python问题：
确保安装了所有依赖并且导入了需要的包。
确保python版本正确

其它：
确保版本正确（基本都为最新版本）

本产品是一个虚拟宠物医院教学软件，能够帮助宠物工作者无需前往实体医院就能系统地学习各种宠物诊疗专业知识。由于近年来宠物医院在国内兴起，然而却缺乏符合资质的宠物医生来满足宠物医疗产业的需求。再加之由于过强的分散性和地域经济相关性，在各地建造实体宠物医生教学和培训机构并不现实。因此，基于互联网的宠物医疗方案，即本产品——虚拟宠物医院学习系统应运而生。虚拟宠物医院学习软件为宠物医院从业者、学生及爱好者提供了一个高度逼真、互动性强的学习环境。通过模拟真实宠物医院的工作流程，帮助用户提高临床处理能力、加深专业知识理解，是宠物医疗领域不可或缺的学习工具。
