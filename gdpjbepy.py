# 导入Flask类
from flask import Flask as _Flask
from flask import request
from condbconfig import Config
import json #post请求传入json对象时，通过json获取参数
from flask import jsonify
from flask_cors import CORS,cross_origin
from flask.json import JSONEncoder as _JSONEncoder
from datetime import date
import random

#导入第三方连接库
from flask_sqlalchemy import SQLAlchemy

# 实例化，可视为固定格式
app = _Flask(__name__)
# 跨域
CORS(app)

app.config.from_object(Config)
# 创建sqlalchemy对象
db = SQLAlchemy(app)

# 判断数字函数
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

# 重写json方法

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder


# 实例化之后需要继承模型,模型就是数据库映射，控制数据库之前必须要继承模型
# users表映射
class users(db.Model):
    __tablename__ = "users"
    account = db.Column(db.String(256),primary_key=True)
    nickname = db.Column(db.String(256),nullable=False)
    sex = db.Column(db.String(256),nullable=False)
    password = db.Column(db.Integer,nullable=False)
    phonenum = db.Column(db.Integer,nullable=False)
    age = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(256),nullable=False)
    # json序列化
    def keys(self):
        return ['account', 'nickname','sex','password','phonenum','age','address']

    def __getitem__(self, item):
        return getattr(self, item)

# articlelist表映射
class articlelist(db.Model):
    __tablename__ = "articlelist"
    briefcontent = db.Column(db.String(256),nullable=False)
    articleid = db.Column(db.Integer,primary_key=True)
    likenum = db.Column(db.Integer,nullable=False) 
    author = db.Column(db.String(256),nullable=False)
    creationtime = db.Column(db.DateTime,nullable=False)
    title = db.Column(db.String(256),nullable=False)
    comnum = db.Column(db.Integer,nullable=False) 
    category = db.Column(db.Integer,nullable=False)
    # json序列化
    def keys(self):
        return ['briefcontent', 'articleid','likenum','author','creationtime','title','comnum','category']

    def __getitem__(self, item):
        return getattr(self, item) 

# article表映射
class article(db.Model):
    __tablename__ = "article"
    content = db.Column(db.String(256),nullable=False)
    articleid = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(256),nullable=False)
    creationtime = db.Column(db.DateTime,nullable=False)
    title = db.Column(db.String(256),nullable=False)
    comnum = db.Column(db.Integer,nullable=False) 
    category = db.Column(db.Integer,nullable=False) 
    likenum = db.Column(db.Integer,nullable=False) 
    # json序列化
    def keys(self):
        return ['content', 'articleid','likenum','author','creationtime','title','comnum','category']

    def __getitem__(self, item):
        return getattr(self, item) 


# route()方法用于设定路由；类似spring路由配置
# 下面是登陆接口实现
@app.route('/Login',methods=['post'])
def Login():
    account = request.json.get('account')
    password = request.json.get('password')
    obj = users.query.filter(users.account == account, users.password == password).first()
    if obj.password == password and obj.account == account:
         return jsonify({"message":"登录成功","result": "success"})
    else:
         return jsonify({"message":"登录失败","result": "failed"})

# 注册接口实现
@app.route('/Register',methods=['post'])
def Register():
    account = request.json.get('account')
    password = request.json.get('password')
    obj = users.query.filter(users.account == account, users.password == password).first()
    if obj == None and password != "":
        newuser = users(account=account, password = password)
        db.session.add(newuser)
        #事务 python gdpjbepy.py
        db.session.commit()
        return jsonify({"message":"注册成功！","result": "success"})
    elif obj.account == account:
        return jsonify({"message":"注册失败，用户已经存在了","result": "failed"})
    elif obj.password == "":
        return jsonify({"message":"注册失败！密码不能为空！","result": "failed"})


# 用户信息更新接口实现
@app.route('/UpdateUserInfor',methods=['post'])
def UpdateUserInfor():
    account = request.json.get('account')
    password = request.json.get('password')
    age = request.json.get('age')
    address = request.json.get('address')
    phonenum = request.json.get('phonenum')
    sex = request.json.get('sex')
    nickname = request.json.get('nickname')
    obj = users.query.filter(users.account == account).first()
    # obj.title = 'new title'
    # db.session.commit()

    # 修改年龄
    if is_number(age) == False or age < 0 or age > 99999999999 or age == "" :
        return jsonify({"message":"修改用户信息失败，用户年龄输入错误！","result": "failed"})
    else :
        obj.age = age
        # db.session.commit()

    # 修改密码
    if password == "":
        return jsonify({"message":"修改用户密码失败，用户密码不能为空","result": "failed"})
    else :
        obj.password = password
    
    # 修改昵称
    if nickname == "":
        return jsonify({"message":"修改用户昵称失败，用户昵称不能为空","result": "failed"})
    else :
        obj.nickname = nickname
    
    # 修改地址
    obj.address = address

    # 修改性别
    if sex != "male" and sex != "female":
        return jsonify({"message":"修改用户性别失败，用户性别只能为male或female","result": "failed"})
    else :
        obj.sex = sex

    # 修改电话号码
    if is_number(phonenum) == False or phonenum < 0 or phonenum > 99999999999 and phonenum != "" :
        return jsonify({"message":"修改用户电话号码失败，用户电话号码只能大于0小于99999999999！","result": "failed"})
    else :
        obj.age = age
        # 最终一次性提交所有数据库修改
        db.session.commit()
        return jsonify({"message":"修改用户信息成功","result": "success"})

# 获取用户信息接口实现
@app.route('/GetUserInfor',methods=['GET'])
def GetUserInfor():
    account = request.values.get('account')
    password = request.values.get('password')
    print(account,password)
    obj = users.query.filter(users.account == account, users.password == password).first()
    data_json = json.loads(json.dumps(obj, cls=JSONEncoder))
    if obj == None:
        return jsonify({"message":"查询失败，用户信息不存在！","result": "failed"})
    else :
        return jsonify({"message":data_json,"result": "success"})

# 获取用户个人文章列表接口实现
@app.route('/GetArticleList',methods=['GET'])
def GetArticleList():
    author = request.args.get('account')
    obj = articlelist.query.filter(articlelist.author == author).all()
    data_json = json.loads(json.dumps(obj, cls=JSONEncoder))
    if obj == None:
        return jsonify({"message":[],"result": "success"})
    else :
        return jsonify({"message":data_json,"result": "success"})

# 获取文章详情接口实现
@app.route('/GetArticleContent',methods=['GET'])
def GetArticleContent():
    articleid = request.args.get('articleid')
    obj = article.query.filter(article.articleid == articleid).first()
    data_json = json.loads(json.dumps(obj, cls=JSONEncoder))
    if obj == None:
        return jsonify({"message":"查询失败，文章不存在！","result": "failed"})
    else :
        return jsonify({"message":data_json,"result": "success"})

# 发表文章接口实现
@app.route('/PostArticle',methods=['POST'])
def PostArticle():
    content = request.json.get('content')
    author = request.json.get('account')
    title = request.json.get('title')
    creationtime = request.json.get('creationtime')
    category = request.json.get('dynamicTags')
    # 生成随机哈希值的文章id
    articleid = random.getrandbits(128) 
    #增加
    newarticle = Article(title=title, content=content,creationtime=creationtime,category=dynamicTags,author=author,articleid=articleid)
    db.session.add(newarticle)
    #提交事务
    db.session.commit()
    # data_json = json.loads(json.dumps(obj, cls=JSONEncoder))
    if obj == None:
        return jsonify({"message":"查询失败，文章不存在！","result": "failed"})
    else :
        return jsonify({"message":"发表文章成功！","result": "success"})


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="127.0.0.1", port=3000, debug=True)


# 运行程序入口：python gdpjbepy.py GetArticleList GetUserInfor