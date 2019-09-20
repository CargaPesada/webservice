import unittest
import sys
import firebase_admin
sys.path.append(".")
from models.User import User
from firebase_admin import credentials

cred = credentials.Certificate("database/credentials.json")
firebase_admin.initialize_app(cred)
valid_user = User({
    'cargo': 'motorista',
    'cpf': None,
    'ddn': None,
    'dependentes': None,
    'email': None,
    'endereco': None,
    'nome': None,
    'nomemae': None,
    'nomepai': None,
    'ocorrencias': None,
    'senha': None,
    'sexo': None,
    'tipocnh': None,
})


class UserTest(unittest.TestCase):
    def test_init_raise(self):
        self.assertRaises(Exception, User, {"test": None})

    def test_init(self):
        self.assertIsInstance(valid_user, User)

    def test_user_cargo(self):
        self.assertRaises(Exception, User, valid_user)


if __name__ == '__main__':
    unittest.main()