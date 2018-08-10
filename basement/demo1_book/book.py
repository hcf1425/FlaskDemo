from flask import Flask, render_template
from flask import flash
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
# from flask_migrate import Migrate,MigrateCommand

import pymysql
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 配置数据库连接地址
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:!@127.0.0.1:3306/booktest9"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)

class ApendForm(FlaskForm):

    authorname = StringField("作者：",validators=[DataRequired("请输入作者姓名")],render_kw={'placeholder':'请输入作者姓名'})
    bookname = StringField("书名：",validators=[DataRequired("请输入书名")],render_kw={'placeholder':'情输入书名!'})
    submit = SubmitField("添加")

class Author(db.Model):

    __tablename__ = 'author'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    books = db.relationship('Book',backref = "author")

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    author_id = db.Column(db.Integer,db.ForeignKey(Author.id))


@app.route("/")
def homepage():
    form = ApendForm()
    authors = Author.query.all()
    return render_template("bookmanagement.html",authors=authors,myform = form)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)