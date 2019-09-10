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
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
