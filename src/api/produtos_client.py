import requests

BASE_URL = "https://compassuol.serverest.dev"


#Responsável por comunicar com a API
class ProdutosClient:
    def __init__(self):
        self.base = f"{BASE_URL}/produtos"

    def listar(self, params=None):
        return requests.get(self.base, params=params)

    def cadastrar(self, payload, token):
        headers = {"Authorization": token} if token else {}
        return requests.post(self.base, json=payload, headers=headers)

    def buscar_por_id(self, produto_id):
        return requests.get(f"{self.base}/{produto_id}")

    def atualizar(self, produto_id, payload, token):
        headers = {"Authorization": token} if token else {}
        return requests.put(f"{self.base}/{produto_id}", json=payload, headers=headers)

    def excluir(self, produto_id, token):
        headers = {"Authorization": token} if token else {}
        return requests.delete(f"{self.base}/{produto_id}", headers=headers)