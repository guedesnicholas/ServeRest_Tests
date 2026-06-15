import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api.usuarios_client import UsuariosClient
from src.api.usuarios_client import ProdutosClient
from src.helpers.factories import payload_usuario_valido
from src.helpers.factories import payload_produto_valido



@pytest.fixture(scope="session")
def client():
    # Cliente HTTP para o endpoint de usuários
    return UsuariosClient()


@pytest.fixture
def usuario_cadastrado(client):
    #fornecer um usuário real na API
    #É criado e destruído a cada teste que o usa 
    payload = payload_usuario_valido()

    resposta = client.cadastrar(payload)

    assert resposta.status_code == 201, (
        f"Falha ao criar usuário. Status: {resposta.status_code} — {resposta.text}"
    )

    usuario_id = resposta.json()["_id"]

    yield {"id": usuario_id, "payload": payload}

    # Cleanup: remove o usuário criado
    client.excluir(usuario_id)


@pytest.fixture(scope="session")
def pclient():
    # Cliente HTTP para o endpoint de usuários
    return ProdutosClient()


@pytest.fixture
def produto_cadastrado(pclient):
    #fornecer um usuário real na API
    #É criado e destruído a cada teste que o usa 
    payload = payload_produto_valido()

    resposta = pclient.cadastrar(payload)

    assert resposta.status_code == 201, (
        f"Falha ao criar usuário. Status: {resposta.status_code} — {resposta.text}"
    )

    usuario_id = resposta.json()["_id"]

    yield {"id": usuario_id, "payload": payload}

    # Cleanup: remove o usuário criado
    client.excluir(usuario_id)