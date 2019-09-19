import unittest
import sys
sys.path.append(".")
from models.User import User 

class UserTest(unittest.TestCase):

    def test_init_raise(self):
        self.assertRaises(Exception, User, {"test":None})
        
    def test_init(self):        
        self.assertIsInstance(
            User({
                    'cargo':None,
                    'cpf':None,
                    'ddn':None,
                    'dependentes':None, 
                    'email':None,
                    'endereco':None,
                    'nome':None,
                    'nomemae':None,
                    'nomepai':None,
                    'ocorrencias':None,
                    'senha':None,
                    'sexo':None,
                    'tipocnh':None,
                }), User)

if __name__ == '__main__':
    unittest.main()