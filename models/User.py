import sys
sys.path.append(".")
from database.interface import FirebaseInterface


class User:
    def __init__(self, dict_user_data):
        self.interface = FirebaseInterface()
        self.user_keys = {
            'cargo': False,
            'cpf': False,
            'ddn': False,
            'dependentes': False,
            'email': False,
            'endereco': False,
            'nome': False,
            'nomemae': False,
            'nomepai': False,
            'ocorrencias': False,
            'senha': False,
            'sexo': False,
            'tipocnh': False
        }

        self.validateUserData(dict_user_data)

    def validateUserData(self, dict_user_data):
        for key, value in dict_user_data.items():
            if key in self.user_keys:
                self.user_keys[key] = True
            else:
                raise Exception(
                    'Usuario possui um campo invalido: {}'.format(key))

        not_found_values = []
        for key, value in self.user_keys.items():
            if not value:
                not_found_values.append(key)

        if len(not_found_values) > 0:
            raise Exception(
                'Usuario deve conter os campos: {}'.format(not_found_values))

        self.validateCargo(dict_user_data['cargo'])

    def validateCargo(self, cargo):
        firebase_jobs = self.interface.getData('const_data', 'jobs')
        if not cargo in firebase_jobs['available']:
            raise Exception('Cargo do usuario invalido: {}'.format(cargo))
