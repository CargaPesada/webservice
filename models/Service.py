class Service:

    def __init__(self, name, price):
        self.nome = name
        self.price = price

    def validateFields(self):
        if self.nome is None:
            raise Exception("Nome não pode ser nulo")

        if self.price is None or self.price <= 0:
            raise Exception("Preço inválido")

