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
            'tipocnh': False,
            'status': False
        }

        self.validateUserData(dict_user_data)

    def validateUserData(self, dict_user_data):
        for key, value in dict_user_data.items():
            if key in self.user_keys:
                self.user_keys[key] = True
            else:
                raise Exception(
                    'Usuario possui um campo inválido: {}'.format(key))

        not_found_values = []
        for key, value in self.user_keys.items():
            if not value:
                not_found_values.append(key)

        if len(not_found_values) > 0:
            raise Exception(
                'Usuario deve conter os campos: {}'.format(not_found_values))

        self.validateCargo(dict_user_data['cargo'])
        self.validateCPF(dict_user_data['cpf'])
        self.validateName(dict_user_data['nomemae'])
        self.validateDDN(dict_user_data['ddn'])
        self.validateFathersName(dict_user_data['nomepai'])
        self.validateName(dict_user_data['nome'])
        self.validateGenre(dict_user_data['sexo'])
        self.vallidateAddress(dict_user_data['endereco'])
        self.vallidateStatus(dict_user_data['status'])

    def validateCargo(self, cargo):
        firebase_jobs = self.interface.getData('const_data', 'jobs')
        if not cargo in firebase_jobs['available']:
            raise Exception('Cargo do usuario inválido: {}'.format(cargo))

    def validateCPF(self, cpf):
        if not cpfcnpj.validate(cpf):
            raise Exception('CPF inválido')

    def validateName(self, name):
        if not re.search("^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$",
                         name):
            raise Exception('Nome {} é inválido'.format(name))

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
            raise Exception('Nome do pai inválido')

    def validateGenre(self, genre):
        if genre != 'm' and genre != 'f':
            raise Exception('Sexo do usuario inválido')

    def vallidateAddress(self, address):
        if not address:
            raise Exception('Endereco inválido')

    def vallidateStatus(self, status):
        if status is not True and status is not False:
            raise Exception('Status inválido')
