from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface


class SchedulesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def post(self):
        req = request.get_json()

        office_id = req["id_oficina"]

        try:
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina não encontrada")

            user_id = req["id_usuario"]
            user = self.interface.getData("users", user_id)

            if user["cargo"] != "mecanico" or user is None:
                raise Exception("Mecânico não encontrado")

            truck_id = req["id_caminhao"]
            truck = self.interface.getData("trucks", truck_id)

            if truck is None:
                raise Exception("Caminhão não encontrado")

            date = req["data"]

            for schedule in office["agenda"]:
                if schedule["data"] == date:
                    raise Exception("Dia solicitado não está disponível")

            title = req["titulo"]

            schedule_request = {
                "id": len(office["agenda"]) + 1,
                "data": date,
                "title": title,
                "mecanico": user,
                "caminhao": truck
            }

            office["agenda"].append(schedule_request)

            self.interface.updateData(office, "offices", office["id"])
            result = "Evento criado com sucesso"
            http_return_code = 201

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code

    def delete(self, office_id, event_id):

        try:
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina fornecida não encontrada")

            event_id = int(event_id) - 1

            if event_id > len(office["agenda"]):
                raise Exception("Id inválido")

            office["agenda"].pop(event_id)

            self.interface.updateData(office, "offices", office["id"])
            result = "Evento removido com sucesso"
            http_return_code = 200

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code
