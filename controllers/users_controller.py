from flask import request
from flask_restful import Resource, reqparse, abort
from database.interface import FirebaseInterface
import json


class UsersController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, user_mail=None):
        if user_mail:
            dic = {"data": self.interface.getData("users", user_mail)}
        else:
            dic = {"data": self.interface.getData("users")}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def post(self):
        http_return_code = 201
        result = request.get_json()

        try:
            self.interface.addData(result, "users", result["email"])
        except:
            http_return_code = 404
            result = "Motoristas devem possuir emails"

        return result, http_return_code
