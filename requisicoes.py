import requests
import os
chave = os.getenv("chaveapi")


class Requisicoes:
    # base_url = "http://petparkapi.pythonanywhere.com/"
    base_url = "http://localhost:5000/"
    def caes_ativos(self):
        ativos = []
        caes_ativos = requests.get(self.base_url+"creche", headers={"tokenapi":chave})
        print(caes_ativos.json())
        for dog in caes_ativos.json():
            # ativos.append(f"{dog['NOME_CAO']}")
            ativos.append(dog)
        ativos.sort(key=lambda item: item.get('NOME_CAO'))
        return ativos

    def get_caes_hotel(self):
        """
        :return: só vai retornar o cão de hotel que ainda não passou a data de saída
        """
        jresposta = requests.get(self.base_url+"hotel", headers={"tokenapi":chave})
        return jresposta.json()

    def postar_caes_creche(self, caesnacreche: dict):
        endpoint = "creche"
        requests.post(self.base_url+endpoint, json=caesnacreche)

    def postar_caes_hotel(self, caesnohotel: dict):
        requests.post(self.base_url+"hotel", json=caesnohotel)


class RequisicoesFunc:
    # base_url = "http://petparkapi.pythonanywhere.com/"
    base_url = "http://localhost:5000/"

    def get_usernames(self):
        endpoint = "/cadastrar-funcionario"
        resposta = requests.get(self.base_url+endpoint, headers={"tokenapi": chave})
        return resposta

    def criar_cadastro(self, pacote):
        endpoint = "/cadastrar-funcionario"
        resposta = requests.post(self.base_url+endpoint, json=pacote)
        return resposta

    def logar(self, credentials):
        endpoint = "login"
        resposta = requests.post(self.base_url+endpoint, json=credentials)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            return 'Credenciais Incorretas'

if __name__ == "__main__":
    requisicao = Requisicoes()
    resposta = requisicao.caes_ativos()
    print(resposta)
