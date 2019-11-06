import json
from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface
from models.Service import Service


class ServicesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        try:
            dic = {"data": self.interface.getData("services")}

            data = json.dumps(dic)
            result = json.loads(data)
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def post(self):
        req = request.get_json()

        try:
            name = req["nome"]
            price = req["preco"]

            service = Service(name, price)
            service.validateFields()

            self.interface.setData(service.__dict__, "services", name)
            result = "Serviço cadastrado com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def delete(self, service):
        try:
            self.interface.deleteData("services", service)

            result = "Serviço removido com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def put(self):
        req = request.get_json()

        try:
            name = req["nome"]
            price = req["preco"]

            service = Service(name, price)
            service.validateFields()

            self.interface.updateData(service.__dict__, "services", name)

            result = "Serviço alterado com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code
