import requests

BASE_URL = "https://compassuol.serverest.dev"


#Responsável por comunicar com a API
class UsuariosClient:
    def __init__(self):
        self.base = f"{BASE_URL}/usuarios"

    def listar(self, params=None):
        return requests.get(self.base, params=params)

    def cadastrar(self, payload):
        return requests.post(self.base, json=payload)

    def buscar_por_id(self, usuario_id):
        return requests.get(f"{self.base}/{usuario_id}")

    def atualizar(self, usuario_id, payload):
        return requests.put(f"{self.base}/{usuario_id}", json=payload)

    def excluir(self, usuario_id):
        return requests.delete(f"{self.base}/{usuario_id}")
