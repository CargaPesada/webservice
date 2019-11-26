import sys
import re
sys.path.append(".")
from pycpfcnpj import cpfcnpj
from database.interface import FirebaseInterface


class Office:
    def __init__(self, dict_office_data):
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

        self.validateOfficeData(dict_office_data)

    def validateOfficeData(self, dict_office_data):
        for key, value in dict_office_data.items():
            if key in self.office_keys:
                self.office_keys[key] = True
            else:
                raise Exception(
                    'Oficina possui um campo inválido: {}'.format(key))

        not_found_values = []
        for key, value in self.office_keys.items():
            if not value:
                not_found_values.append(key)

        if len(not_found_values) > 0:
            raise Exception(
                'Usuario deve conter os campos: {}'.format(not_found_values))

        self.validateCPF(dict_office_data['cpf'])
        self.validateTel(dict_office_data['telefone'])
        self.validateCep(dict_office_data['endereco']['CEP'])
        self.validateName(dict_office_data['endereco']['bairro'])
        self.validateName(dict_office_data['endereco']['cidade'])
        self.validateName(dict_office_data['endereco']['estado'])
        self.validateNumber(dict_office_data['endereco']['numero'])
        self.validatePais(dict_office_data['endereco']['pais'])
        self.validateName(dict_office_data['endereco']['rua'])

    def validateCPF(self, cpf):
        if not cpfcnpj.validate(cpf):
            raise Exception('CPF inválido')
        else:
            allow = ["supervisor", "gerente", "diretor"]
            user = self.interface.getDataByField('users', 'cpf', cpf)
            if not user:
                raise Exception('Não foi encontrado usuário com esse cpf')
            print (user)
            c = 0
            for a in allow:
                if a in str(user):
                    c += 1
            if c == 0:
                raise Exception('Esse usuário não tem permissão')

    def validateName(self, name):
        if not re.search("^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$",
                         name):
            raise Exception('Campo {} é inválido'.format(name))

    def validateNumber(self, num):
        if not re.search("\d+", num):
            raise Exception('Número inválido'.format(num))

    def validateTel(self, tel):
        if not re.search("(\(?\d{2}\)?\s?)(\d{4,6}\-?\d{4})", tel):
            raise Exception('Telefone inválido'.format(tel))

    def validateCep(self, cep):
        if not re.search("\d{5}-\d{3}", cep):
            raise Exception('CEP inválido'.format(cep))

    def validatePais(self, pais):
        list_paises = self.interface.getData('const_data', 'countries')

        if pais not in list_paises['available']:
            raise Exception('País inválido {}'.format(pais))