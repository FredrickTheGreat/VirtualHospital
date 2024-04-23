from flask import Flask, session, g, jsonify
from flask_cors import CORS
from exts import db
from models import User
import setting

app = Flask(__name__, static_url_path='/static')
# 允许跨域传输数据
CORS(app)
app.config.from_object(setting)
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024  # 16MB
db.init_app(app)


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "文件太大，请上传小于16MB的文件。"}), 413


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)
