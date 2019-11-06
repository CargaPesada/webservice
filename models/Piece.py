class Piece:

    def __init__(self, name, price, uni):
        self.nome = name
        self.price = price
        self.uni = uni

    def validateFields(self):
        if self.nome is None:
            raise Exception("Nome não pode ser nulo")

        if self.price is None or self.price <= 0:
            raise Exception("Preço inválido")
        
        if self.uni is None:
            raise Exception("Unidade não pode ser nula")
