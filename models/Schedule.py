from database.interface import FirebaseInterface


class Schedule:

    def __init__(self):
        self.id = None
        self.titulo = None
        self.data = None
        self.caminhao = None
        self.mecanico = None

    def validateFields(self, office_schedule):
        if self.titulo is None:
            raise Exception("Título não informado")

        if self.data is None:
            raise Exception("Data não informada")
        else:
            for event in office_schedule:
                if event["data"] == self.data:
                    raise Exception("Dia solicitado não está disponível")

        if self.caminhao is None:
            raise Exception("Caminhão não encontrado")

        if self.mecanico is None or self.mecanico["cargo"] != "mecanico":
            raise Exception("Mecânico não encontrado")

    def buildObject(self, req):
        interface = FirebaseInterface()

        user_id = req["id_usuario"]
        self.mecanico = interface.getData("users", user_id)

        truck_board = req["placa_caminhao"]
        self.caminhao = interface.getDataByField("trucks", "placa", truck_board)

        self.data = req["data"]

        self.titulo = req["titulo"]

    def setId(self):
        interface = FirebaseInterface()

        event_id = interface.getData("const_data", "office_id")
        self.id = event_id["id"] + 1
        interface.updateData({"id": event_id["id"] + 1}, "const_data", "office_id")

    @staticmethod
    def findIdIndex(id, office):
        for index in range(len(office)):
            if office[index]["id"] == id:
                return index
            elif index + 1 == len(office) and office[index]["id"] != id:
                raise Exception("Id inválido")
