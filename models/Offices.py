import sys
import re
import json
sys.path.append(".")
from pycpfcnpj import cpfcnpj
from database.interface import FirebaseInterface


class Office:
    def __init__(self, dict_office_data):
        self.dict_office_data = dict_office_data
        self.interface = FirebaseInterface()
        self.office_keys = {
            'cpf': False,
            'endereco': {
                'CEP': False,
                'bairro': False,
                'cidade': False,
                'complemento': False,
                'estado': False,
                'numero': False,
                'pais': False,
                'rua': False
            },
            'nome': False,
            'telefone': False
        }
        self.office_result = {
            'cpf': False,
            'endereco': {
                'CEP': False,
                'bairro': False,
                'cidade': False,
                'complemento': False,
                'estado': False,
                'numero': False,
                'pais': False,
                'rua': False
            },
            'nome': False,
            'telefone': False
        }

    def validateOfficeData(self):
        for key, value in self.dict_office_data.items():
            if key in self.office_keys:
                self.office_keys[key] = True
            else:
                raise Exception(
                    'Usuario possui um campo inválido: {}'.format(key))

        for key, value in self.office_keys.items():
            if not value:
                self.office_result[key] = 404

        self.office_result['cpf'] = self.validateCPF(self.dict_office_data['cpf'])
        self.office_result['nome'] = self.validateName(self.dict_office_data['nome'])
        self.office_result['telefone'] = self.validateTel(self.dict_office_data['telefone'])
        print(self.office_result)
        self.office_result['endereco']['CEP'] = self.validateCep(self.dict_office_data['endereco']['CEP'])
        print(self.office_result)
        self.office_result['endereco']['bairro'] = self.validateName(self.dict_office_data['endereco']['bairro'])
        self.office_result['endereco']['cidade'] = self.validateName(self.dict_office_data['endereco']['cidade'])
        self.office_result['endereco']['estado'] = self.validateName(self.dict_office_data['endereco']['estado'])
        self.office_result['endereco']['numero'] = self.validateNumber(self.dict_office_data['endereco']['numero'])
        self.office_result['endereco']['pais'] = self.validateName(self.dict_office_data['endereco']['pais'])
        self.office_result['endereco']['rua'] = self.validateName(self.dict_office_data['endereco']['rua'])

        print (self.office_result)
        data = json.dumps(self.office_result)
        data_json = json.loads(data)
        return data_json

    def validateCPF(self, cpf):
        if not cpfcnpj.validate(cpf):
            return 400
        else:
            supervisor = self.interface.getDataByField('users', 'cpf', cpf)
            print (supervisor.to_dict())
            if not supervisor:
                return 400

    def validateName(self, name):
        if not re.search("[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$",
                         name):
            return 400

    def validateNumber(self, num):
        if not re.search("\d+", num):
            return 400

    def validateTel(self, tel):
        print("aaaaaaaa")
        if not re.search("(\(?\d{2}\)?\s?)(\d{4,5}\-?\d{4})", tel):
            return 400

    def validateCep(self, cep):
        if not re.search("\d{5}-\d{3}", cep):
            return 400

    def validatePais(self, pais):
        list_pais = self.interface.getData('const_data', 'countries')

        if pais not in list_pais['available']:
            return 400