import requests

BASE_URL = "https://compassuol.serverest.dev"


#Responsável por comunicar com a API
class ProdutosClient:
    def __init__(self):
        self.base = f"{BASE_URL}/produtos"

    def listar(self, params=None):
        return requests.get(self.base, params=params)

    def cadastrar(self, payload):
        return requests.post(self.base, json=payload)

    def buscar_por_id(self, produtos_id):
        return requests.get(f"{self.base}/{produtos_id}")

    def atualizar(self, produtos_id, payload):
        return requests.put(f"{self.base}/{produtos_id}", json=payload)

    def excluir(self, produtos_id):
        return requests.delete(f"{self.base}/{produtos_id}")
