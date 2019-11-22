from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface
from models.Schedule import Schedule


class SchedulesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def post(self):
        req = request.get_json()

        try:
            self.validateRequest(req)

            schedule = Schedule(req)

            if schedule.id is None:
                event_id = self.interface.getData("const_data", "office_id")
                schedule.id = int(event_id["id"]) + 1

            office = self.interface.getData("offices", schedule.oficina)

            if office is None:
                raise Exception("Oficina informada não encontrada")
            else:
                office["agenda"].append(str(schedule.id))

            schedule_date = self.interface.getDataByTwoFields("schedules", "data", schedule.data, "oficina", schedule.oficina)

            if schedule_date:
                raise Exception("Esta oficina já possui evento para essa data")

            user = self.interface.getData("users", schedule.mecanico)

            if user is None:
                raise Exception("Mecânico não encontrado")
            elif user["cargo"] != "mecanico":
                raise Exception("Usuário fornecido possui o cargo de " + user["cargo"] + " e não o de mecânico")

            truck = self.interface.getDataByField("trucks", "placa", schedule.caminhao)

            if truck is None:
                raise Exception("Nenhum caminhão foi encontrado com essa placa")
            else:
                schedule.caminhao = truck[0]["id"]

            self.interface.setData(schedule.__dict__, "schedules", str(schedule.id))
            self.interface.updateData(office, "offices", schedule.oficina)
            self.interface.updateData({"id": schedule.id}, "const_data", "office_id")

            result = "Evento criado com sucesso"
            http_return_code = 201

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code

    @staticmethod
    def validateRequest(req):
        expected_request = {"titulo",
                            "data",
                            "id_oficina",
                            "id_usuario",
                            "placa_caminhao"}

        keys_not_found = []

        for key in expected_request:
            if key not in req:
                keys_not_found.append(key)

        if keys_not_found.__len__() == 1:
            raise Exception("O campo " + keys_not_found[0] + " deve ser enviado")
        elif keys_not_found.__len__() > 1:
            raise Exception("Os seguintes campos estão faltando: " + ", ".join(keys_not_found))
