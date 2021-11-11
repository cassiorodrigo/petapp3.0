import unittest
from dbmanager import Conexao
from datavalidators import validate_email_basic
from requisicoes import RequisicoesFunc



class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_email = validate_email_basic("cassiorodrigo@gmail.com")
        # self.nova_conn = Conexao()
        # self.tabela = self.nova_conn.conectar()

    def test_email_val(self):
        self.assertTrue(self.valid_email)
        print(self.valid_email)
        # resposta_hotel = self.req.get_caes_hotel()
        # print(f"Resposta hotel: {resposta_hotel}")
        # self.assertEqual(True, False)  # add assertion here

    def test_logar(self):
        novareq = RequisicoesFunc()
        resposta = novareq.logar({"usuario": "digo", "senha": "senha de testes"})
        print(resposta.json())


if __name__ == '__main__':
    unittest.main()
