from flask import request
from flask_restful import Resource, reqparse, abort
from database.interface import FirebaseInterface
import json
import sys

sys.path.append(".")
from models.User import User


class UsersController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        dic = {"data": self.interface.getData("users")}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def post(self):
        http_return_code = 201
        result = request.get_json()

        try:
            User(result)
            self.interface.addData(result, "users", result["email"])
        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code

    def put(self):
        http_return_code = 200
        result = request.get_json()

        cpf = result["cpf"]
        status = result["status"]

        try:
            user = self.interface.getDataByField("users", "cpf", cpf)

            if user:
                user[0]["status"] = status
                self.interface.updateData(user[0], "users", user[0]["id"])
                result = "Status atualizado com sucesso"
            else:
                result = "Usuario não encontrado"
                http_return_code = 400

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code


class UsersControllerById(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, user_mail):
        dic = {"data": self.interface.getData("users", user_mail)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def delete(self, user_mail):
        self.interface.deleteData("users", user_mail)

    def put(self, user_mail):
        result = request.get_json()
        http_return_code = 200

        try:
            User(result)
            self.interface.addData(result, "users", user_mail)
        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code


class UsersControllerByRegion(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, region):
        dic = {"data": self.interface.getDataByField("users", "pais", region)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json
