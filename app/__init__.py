from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
# from flask_admin import Admin


app = Flask(__name__)

app.config["PAGE_SIZE"] = 3

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name="duiwbkm7z",
    api_key="353275184747744",
    api_secret="W1pyuWAbgKE-Qcvw1kg1mxuyh0w",
    secure=True
)

app.secret_key="ashdfsajflksadl;fa;sflsajl-1312"
login = LoginManager(app=app)

