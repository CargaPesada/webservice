class Schedule:

    def __init__(self, req):
        self.id = None if req.get("id") is None else req["id"]
        self.titulo = req["titulo"]
        self.data = req["data"]
        self.oficina = req["id_oficina"]
        self.mecanico = req["id_usuario"]
        self.caminhao = req["placa_caminhao"]

        self.validateScheduleData()

    def validateScheduleData(self):
        if self.titulo is None or not self.titulo:
            raise Exception("Titulo do evento não pode ser nulo")

        if self.data is None or not self.data:
            raise Exception("Data do evento não pode ser nula")

        if self.oficina is None or not self.oficina:
            raise Exception("Oficina onde o evento ocorrerá não pode ser nula")

        if self.mecanico is None or not self.mecanico:
            raise Exception("Mecânico que realizará a manutenção não pode ser nulo")

        if self.caminhao is None or not self.caminhao:
            raise Exception("Placa do caminhão não pode ser nula")
