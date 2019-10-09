from firebase_admin import auth
from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface
import json
from models.Offices import Office


class OfficesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        dic = {"data": self.interface.getData("offices")}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def post(self):
        http_return_code = 201
        result = request.get_json()

        try:
            Office(result)
            self.interface.addData(result, "offices", None)
        except Exception as e:
            http_return_code = 400
            result = str(e)
        return result, http_return_code


class OfficeControllerById(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, office_id):
        dic = {"data": self.interface.getData("offices", office_id)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def delete(self, office_id):
        self.interface.deleteData("offices", office_id)

    def put(self, office_id):
        http_return_code = 201
        result = request.get_json()

        try:
            Office(result)
            self.interface.addData(result, "offices", office_id)
        except Exception as e:
            http_return_code = 400
            result = str(e)
        return result, http_return_code


class OfficeControllerByRegion(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, region):
        dic = {"data": self.interface.getDataByField("offices", "pais", region)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json


class OfficeControllerByUser(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, cpf):
        dic = {"data": self.interface.getDataByField("offices", "cpf", cpf)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json











