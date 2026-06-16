import pytest
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.api.usuarios_client import UsuariosClient
from src.api.produtos_client import ProdutosClient
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
def produto_cadastrado(pclient, token): 
    # fornecer um produto real na API
    # é criado e destruído a cada teste que o usa
    payload = payload_produto_valido()

    resposta = pclient.cadastrar(payload, token)  

    assert resposta.status_code == 201, (
        f"Falha ao criar produto. Status: {resposta.status_code} — {resposta.text}"
    )

    produto_id = resposta.json()["_id"]

    yield {"id": produto_id, "payload": payload}

    # Cleanup
    pclient.excluir(produto_id, token)  


@pytest.fixture(scope="session") #evita múltiplos logins
def token(client):
    # Arrange
    payload = {
        "nome": "Usuario Admin",
        "email": f"auth_{uuid.uuid4().hex[:8]}@qa.com",
        "password": "senha123",
        "administrador": "true",
    }
    criacao = client.cadastrar(payload)
    usuario_id = criacao.json()["_id"]

    # Act
    resposta = client.login({
        "email": payload["email"],
        "password": payload["password"],
    })

    token = resposta.json()["authorization"]

    yield token  # entrega o token para os testes

    # Cleanup
    client.excluir(usuario_id)

@pytest.fixture(scope="session")
def token_nao_admin(client):
    payload = {
        "nome": "Usuario Comum",
        "email": f"comum_{uuid.uuid4().hex[:8]}@qa.com",
        "password": "senha123",
        "administrador": "false",  
    }
    criacao = client.cadastrar(payload)
    usuario_id = criacao.json()["_id"]

    resposta = client.login({
        "email": payload["email"],
        "password": payload["password"],
    })

    token = resposta.json()["authorization"]

    yield token

    client.excluir(usuario_id)