import unittest
from dbmanager import Conexao


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.nova_conn = Conexao()
        self.tabela = self.nova_conn.conectar()

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def tearDownClass(cls) -> None:
        pass

if __name__ == '__main__':
    unittest.main()
