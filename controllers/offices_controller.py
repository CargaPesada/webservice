from flask import request
from flask_restful import Resource, reqparse, abort
from database.interface import FirebaseInterface
import json


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
        result = request.get_json()
        self.interface.addData(result, "offices", None)


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
        result = request.get_json()
        self.interface.addData(result, "offices", office_id)


class OfficeControllerByRegion(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, region):
        dic = {"data": self.interface.getDataByField("offices", 'country', region)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json
