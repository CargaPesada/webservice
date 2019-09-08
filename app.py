from flask import Flask
from flask_restful import Resource, Api
from controllers import users_controller

app = Flask(__name__)
api = Api(app)

api.add_resource(users_controller.UsersController,
                 '/users/register', '/users/<user_id>', '/users/all')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
