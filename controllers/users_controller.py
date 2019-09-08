from flask import request
from flask_restful import Resource, reqparse, abort


class UsersController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.USERS = {'rodrigo': {'asd': 'asd'}}

    def get(self, user_id=None):
        if(user_id):
            self.abort_if_user_doesnt_exist(user_id)
            result = self.USERS[user_id]
        else:
            result = "All users"

        return result

    def post(self):
        user = {'user': request.get_json()}
        return user, 201

    def abort_if_user_doesnt_exist(self, user_id):
        if user_id not in self.USERS:
            abort(404, message="User {} does not exist.".format(user_id))
