from flask import request
from flask_restful import Resource, reqparse, abort
from database.interface import FirebaseInterface
import json


class OfficesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        try:
            dic = {"mensagem": "Oficinas retornadas com sucesso", "data": self.interface.getData("offices")}
        except:
            dic = {"mensagem": "Erro ao retornar oficinas"}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def post(self):
        result = request.get_json()
        try:
            self.interface.addData(result, "offices", None)
            dic = {"mensagem": "Oficina cadastrada com sucesso"}
        except:
            dic = {"mensagem": "Erro ao cadastrar oficina"}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json


class OfficeControllerById(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, office_id):
        try:
            dic = {"mensagem": "Oficina listada com sucesso", "data": self.interface.getData("offices", office_id)}
        except:
            dic = {"mensagem": "Erro ao retornar oficina"}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def delete(self, office_id):
        try:
            self.interface.deleteData("offices", office_id)
            dic = {"mensagem": "Oficina deletada com sucesso"}
        except:
            dic = {"mensagem": "Erro ao deletar oficina"}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json

    def put(self, office_id):
        result = request.get_json()
        try:
            self.interface.addData(result, "offices", office_id)
            dic = {"mensagem": "Oficina atualizada com sucesso"}
        except:
            dic = {"mensagem": "Erro ao atualizar oficina"}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json


class OfficeControllerByRegion(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, region):
        try:
            dic = {"mensagem": "Oficinas da região "+region + " retornadas com sucesso", "data": self.interface.getDataFromField("offices", 'regiao', region)}
        except:
            dic = {"mensagem": "Erro ao retornar oficinas da região "+region}

        data = json.dumps(dic)
        data_json = json.loads(data)
        return data_json
