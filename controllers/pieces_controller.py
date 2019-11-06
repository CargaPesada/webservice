import json
from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface
from models.Piece import Piece


class PiecesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self):
        try:
            dic = {"data": self.interface.getData("pieces")}

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
            uni = req["uni"]
            piece = Piece(name, price, uni)
            piece.validateFields()

            self.interface.setData(piece.__dict__, "pieces", name)
            result = "Peça cadastrada com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def delete(self, piece):
        try:
            self.interface.deleteData("pieces", piece)

            result = "Peça removida com sucesso"
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
            uni = req["uni"]

            piece = Piece(name, price, uni)
            piece.validateFields()

            self.interface.updateData(piece.__dict__, "pieces", name)

            result = "Peça alterada com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code
