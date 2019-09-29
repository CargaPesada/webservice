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
        self.user_result = {
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
                    'Usuario possui um campo inválido: {}'.format(key))

        for key, value in self.user_keys.items():
            if not value:
                self.user_keys[key] = 404

        self.validateCargo(dict_user_data['cargo'], 'cargo')
        self.validateCPF(dict_user_data['cpf'], 'cpf')
        self.validateName(dict_user_data['nomemae'], 'nomemae')
        self.validateDDN(dict_user_data['ddn'], 'ddn')
        self.validateFathersName(dict_user_data['nomepai'], 'nomepai')
        self.validateName(dict_user_data['nome'], 'nome')
        self.validateGenre(dict_user_data['sexo'], 'sexo')
        self.vallidateAddress(dict_user_data['endereco'], 'endereco')

    def validateCargo(self, cargo, key):
        firebase_jobs = self.interface.getData('const_data', 'jobs')
        if not cargo in firebase_jobs['available']:
            self.user_keys[key] = 400

    def validateCPF(self, cpf, key):
        if not cpfcnpj.validate(cpf):
            self.user_keys[key] = 400

    def validateName(self, name, key):
        if not re.search("^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$",
                         name):
            self.user_keys[key] = 400

    def validateDDN(self, ddn, key):
        try:
            date = datetime.datetime.strptime(ddn, '%d/%m/%Y')
            if (date.year > 2000 or date.year < 1919):
                raise Exception
        except:
            self.user_keys[key] = 400

    def validateFathersName(self, fathersName, key):
        if fathersName and not re.search(
                "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$", fathersName):
            self.user_keys[key] = 400

    def validateGenre(self, genre, key):
        if genre != 'm' and genre != 'f':
            self.user_keys[key] = 400

    def vallidateAddress(self, address, key):
        if not address:
            self.user_keys[key] = 400