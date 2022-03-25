#Nama Kelompok :
#1 Efendi Kisnoto   19090057
#2 Abbror Sholakhudin 19090141

# Kelas 6A

from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db_user.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "XXXXXX"

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

db.create_all()

class signup(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"success" : True}), 200)
        return jsonify({"success" : False,"msg":"Username dan Password harus diisi"})

class Login(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:

            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"success" : True, "token":token}), 200)
        return jsonify({"success" : False})

api.add_resource(signup, "/api/signup", methods=["POST"])
api.add_resource(Login, "/api/login", methods=["POST"])

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True , port=4000)