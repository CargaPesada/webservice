import sys
import re
import datetime
sys.path.append(".")
from database.interface import FirebaseInterface
from pycpfcnpj import cpfcnpj


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
        self.validateCPF(dict_user_data['cpf'])
        self.validateMothersName(dict_user_data['nomemae'])
        self.validateDDN(dict_user_data['ddn'])
        self.validateFathersName(dict_user_data['nomepai'])

    def validateCargo(self, cargo):
        firebase_jobs = self.interface.getData('const_data', 'jobs')
        if not cargo in firebase_jobs['available']:
            raise Exception('Cargo do usuario invalido: {}'.format(cargo))

    def validateCPF(self, cpf):
        if not cpfcnpj.validate(cpf):
            raise Exception('CPF invalido')

    def validateMothersName(self, mothersName):
        if not re.search("^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$",
                         mothersName):
            raise Exception('Nome da mae invalido')

    def validateDDN(self, ddn):
        try:
            date = datetime.datetime.strptime(ddn, '%d/%m/%Y')
            if (date.year > 2000 or date.year < 1919):
                raise Exception
        except:
            raise Exception('Data de nascimento invalida')

    def validateFathersName(self, fathersName):
        if fathersName and not re.search(
                "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$", fathersName):
            raise Exception('Nome do pai invalido')
