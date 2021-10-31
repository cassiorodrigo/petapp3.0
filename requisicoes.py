import requests

class Requisicoes:
    base_url = "http://petparkapi.pythonanywhere.com/"
    def caes_ativos(self):
        caes_ativos = requests.get()