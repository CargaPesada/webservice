from flask import request
from flask_restful import reqparse, Resource
import json

from database.interface import FirebaseInterface


class TrucksController(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        dic = {"data": self.interface.getData("trucks")}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def post(self):
        result = request.get_json()
        self.interface.addData(result, "trucks", None)


class TrucksControllerById(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, truck_id):
        dic = {"data": self.interface.getData("trucks", truck_id)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def delete(self, truck_id):
        self.interface.deleteData("trucks", truck_id)

    def put(self, truck_id):
        result = request.get_json()
        self.interface.addData(result, "trucks", truck_id)


class TrucksControllerByRegion(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, region):
        dic = {"data": self.interface.getDataByField("trucks", "pais", region)}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json
