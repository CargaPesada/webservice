import firebase_admin
from flask import Flask
from flask_restful import Resource, Api
from controllers import users_controller
from firebase_admin import credentials

app = Flask(__name__)
api = Api(app)
cred = credentials.Certificate("database/credentials.json")
firebase_admin.initialize_app(cred)

api.add_resource(users_controller.UsersController,
                 '/users/register', '/users/<user_mail>', '/users/all')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
