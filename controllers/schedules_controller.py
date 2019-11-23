import json

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

            office = self.getOffice(schedule)
            self.validateOffice(office)

            self.validateDate(schedule)
            self.validateUser(schedule.mecanico)

            truck = self.getTruck(schedule.caminhao)
            self.validateTruck(truck)
            schedule.caminhao = truck

            self.interface.setData(schedule.__dict__, "schedules", str(schedule.id))
            self.interface.addItemToArray("offices", office["id"], "agenda", schedule.id)
            self.interface.updateData({"id": schedule.id}, "const_data", "office_id")

            result = "Evento criado com sucesso"
            http_return_code = 201

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code

    def delete(self, schedule_id):
        try:
            schedule = self.interface.getData("schedules", schedule_id)

            if schedule is None:
                raise Exception("Evento inválido")

            self.interface.deleteItemFromArray("offices", schedule["oficina"], "agenda", schedule_id)
            self.interface.deleteData("schedules", schedule_id)

            result = "Evento deletado com sucesso"
            http_return_code = 201

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def put(self):
        req = request.get_json()

        try:
            self.validateRequest(req)

            schedule = Schedule(req)

            if schedule.id is None:
                raise Exception("O campo id deve ser enviado")
            else:
                previous_schedule = self.interface.getData("schedules", str(schedule.id))

            if schedule.data != previous_schedule["data"] and schedule.oficina == previous_schedule["oficina"]:
                self.validateDate(schedule)

            self.validateUser(schedule.mecanico)

            truck = self.getTruck(schedule.caminhao)
            self.validateTruck(truck)
            schedule.caminhao = truck

            if previous_schedule["oficina"] != schedule.oficina:
                self.interface.deleteItemFromArray("offices", previous_schedule["oficina"], "agenda", schedule.id)

                office = self.getOffice(schedule)
                self.validateOffice(office)

                self.interface.addItemToArray("offices", office["id"], "agenda", schedule.id)

            self.interface.updateData(schedule.__dict__, "schedules", str(schedule.id))

            result = "Evento atualizado com sucesso"
            http_return_code = 201

        except Exception as e:
            result = str(e)
            http_return_code = 400

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

    def getOffice(self, schedule):
        return self.interface.getData("offices", schedule.oficina)

    def validateDate(self, schedule):
        schedule_date = self.interface.getDataByTwoFields("schedules", "data", schedule.data, "oficina",
                                                          schedule.oficina)

        if schedule_date:
            raise Exception("Esta oficina já possui evento para essa data")

    def validateUser(self, mecanico):
        user = self.interface.getData("users", mecanico)

        if user is None:
            raise Exception("Mecânico não encontrado")
        elif user["cargo"] != "mecanico":
            raise Exception("Usuário fornecido possui o cargo de " + user["cargo"] + " e não o de mecânico")

    def getTruck(self, caminhao):
        truck = self.interface.getDataByField("trucks", "placa", caminhao)

        return truck[0]["id"]

    @staticmethod
    def validateTruck(truck):
        if truck is None:
            raise Exception("Nenhum caminhão foi encontrado com essa placa")

    @staticmethod
    def validateOffice(office):
        if office is None:
            raise Exception("Oficina informada não encontrada")


class SchedulesControllerByOffice(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, office_id):
        try:
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina forncecida não encontrada")

            dic = {"data": self.interface.getDataByField("schedules", "oficina", office_id)}

            data = json.dumps(dic)
            result = json.loads(data)
            http_return_code = 201

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code


class SchedulesControllerByMechanic(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()

    def get(self, user_id):
        try:
            user = self.interface.getData("users", user_id)

            if user is None:
                raise Exception("Usuário não encontrado no sistema")
            elif user["cargo"] != "mecanico":
                raise Exception("Usuário deve ser mecânico")

            dic = {"data": self.interface.getDataByField("schedules", "mecanico", user_id)}

            data = json.dumps(dic)
            result = json.loads(data)
            http_return_code = 201

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code
