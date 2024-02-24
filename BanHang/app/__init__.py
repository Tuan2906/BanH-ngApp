from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "tuandeptrai123"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/quan_ly?charset=utf8mb4' % quote(
    "29062003t@")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2
db = SQLAlchemy(app)
login = LoginManager(app=app)
