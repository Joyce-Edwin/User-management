from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import datetime, timedelta


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:Mdelisa2@localhost/manage'
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


