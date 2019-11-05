from flask import request
from flask_restful import Resource, reqparse
from database.interface import FirebaseInterface
import json
from models.Schedule import Schedule


class SchedulesController(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.interface = FirebaseInterface()
        self.schedule = Schedule()

    def post(self):
        req = request.get_json()

        try:
            office_id = req["id_oficina"]
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina não encontrada")

            self.schedule.buildObject(req)
            self.schedule.validateFields(office["agenda"])
            self.schedule.setId()

            office["agenda"].append(self.schedule.__dict__)
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
                raise Exception("Oficina não encontrada")

            index = self.schedule.findIdIndex(int(event_id), office["agenda"])
            office["agenda"].pop(index)

            self.interface.updateData(office, "offices", office_id)

            result = "Evento removido com sucesso"
            http_return_code = 200

        except Exception as e:
            http_return_code = 400
            result = str(e)

        return result, http_return_code

    def get(self, office_id):
        try:
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina não encontrada")

            schedule = {"data": office["agenda"]}

            data = json.dumps(schedule)
            result = json.loads(data)
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code

    def put(self):
        req = request.get_json()

        try:
            office_id = req["id_oficina"]
            office = self.interface.getData("offices", office_id)

            if office is None:
                raise Exception("Oficina não encontrada")

            self.schedule.buildObject(req)
            self.schedule.validateFields(office["agenda"])

            id = req["id_evento"]
            index = self.schedule.findIdIndex(id, office["agenda"])
            self.schedule.id = id

            office["agenda"][index] = self.schedule.__dict__
            self.interface.updateData(office, "offices", office_id)

            result = "Evento alterado com sucesso"
            http_return_code = 200

        except Exception as e:
            result = str(e)
            http_return_code = 400

        return result, http_return_code
