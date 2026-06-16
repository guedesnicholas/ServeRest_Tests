import pytest
import uuid
from src.helpers.factories import payload_produto_valido
from jsonschema import validate
from src.helpers.schemas import SCHEMA_LISTA_PRODUTOS, SCHEMA_PRODUTO, SCHEMA_PRODUTO_ERRADO

@pytest.mark.produtos
class TestListarProdutos:
    def test_listar_produtos_retorna_200_e_lista(self, pclient):
        # Arrange + Act
        resposta = pclient.listar()

        # Assert
        assert resposta.status_code == 200
        corpo = resposta.json()
        assert "quantidade" in corpo
        assert "produtos" in corpo
        assert isinstance(corpo["produtos"], list)
        validate(instance=resposta.json(), schema=SCHEMA_LISTA_PRODUTOS)  # Vai validar o json

@pytest.mark.produtos
class TestCadastrarProduto:
    def test_cadastrar_produto_valido_retorna_201_com_id(self, pclient, produto_cadastrado):
        # Arrange — produto já criado pela fixture

        # Act 
        resposta = pclient.buscar_por_id(produto_cadastrado["id"])

        # Assert
        assert resposta.status_code == 200
        assert "_id" in resposta.json()

    def test_cadastrar_produto_sem_token_retorna_401(self, pclient):
        # Arrange
        payload = payload_produto_valido()

        # Act — cadastra sem passar token
        resposta = pclient.cadastrar(payload, token=None)

        # Assert
        assert resposta.status_code == 401

    def test_cadastrar_produto_com_nome_duplicado_retorna_400(self, pclient, token):
        # Arrange 
        payload = payload_produto_valido()
        criacao = pclient.cadastrar(payload, token)
        assert criacao.status_code == 201
        produto_id = criacao.json()["_id"]

        payload_duplicado = payload_produto_valido()
        payload_duplicado["nome"] = payload["nome"]

        # Act
        resposta = pclient.cadastrar(payload_duplicado, token)

        # Assert
        assert resposta.status_code == 400

        # Cleanup
        pclient.excluir(produto_id, token)

    def test_cadastrar_produto_sem_nome_retorna_400(self, pclient, token):
        # Arrange
        payload = payload_produto_valido()
        del payload["nome"]

        # Act
        resposta = pclient.cadastrar(payload, token)

        # Assert
        assert resposta.status_code == 400

    def test_cadastrar_produto_sem_preco_retorna_400(self, pclient, token):
        # Arrange
        payload = payload_produto_valido()
        del payload["preco"]

        # Act
        resposta = pclient.cadastrar(payload, token)

        # Assert
        assert resposta.status_code == 400

    def test_cadastrar_produto_sem_descricao_retorna_400(self, pclient, token):
        # Arrange
        payload = payload_produto_valido()
        del payload["descricao"]

        # Act
        resposta = pclient.cadastrar(payload, token)

        # Assert
        assert resposta.status_code == 400

    def test_cadastrar_produto_sem_quantidade_retorna_400(self, pclient, token):
        # Arrange
        payload = payload_produto_valido()
        del payload["quantidade"]

        # Act
        resposta = pclient.cadastrar(payload, token)

        # Assert
        assert resposta.status_code == 400
    
    def test_cadastrar_produto_com_token_nao_admin_retorna_403(self, pclient, token_nao_admin):
        # Arrange
        payload = payload_produto_valido()
        # Act
        resposta = pclient.cadastrar(payload, token_nao_admin)
         # Assert
        assert resposta.status_code == 403


@pytest.mark.produtos
class TestBuscarProdutoPorId:
    def test_buscar_produto_existente_retorna_200(self, pclient, produto_cadastrado):
        # Arrange
        produto_id = produto_cadastrado["id"]

        # Act
        resposta = pclient.buscar_por_id(produto_id)

        # Assert
        assert resposta.status_code == 200
        validate(instance=resposta.json(), schema=SCHEMA_PRODUTO)  # Vai validar o json

    def test_buscar_produto_inexistente_retorna_400(self, pclient):
        # Arrange
        id_inexistente = "abcdefghijklmnop"

        # Act
        resposta = pclient.buscar_por_id(id_inexistente)

        # Assert
        assert resposta.status_code == 400
        validate(instance=resposta.json(), schema=SCHEMA_PRODUTO_ERRADO)  # Vai validar o json


@pytest.mark.produtos
class TestAtualizarProduto:
    def test_atualizar_produto_existente_retorna_200(self, pclient, token):
        # Arrange 
        payload = payload_produto_valido()
        criacao = pclient.cadastrar(payload, token)
        assert criacao.status_code == 201
        produto_id = criacao.json()["_id"]

        payload_atualizado = {
            "nome": f"Produto Atualizado {uuid.uuid4().hex[:8]}",
            "preco": 200,
            "descricao": "Produto atualizado por teste automatizado",
            "quantidade": 20,
        }

        # Act
        resposta = pclient.atualizar(produto_id, payload_atualizado, token)

        # Assert
        assert resposta.status_code == 200

        # Cleanup
        pclient.excluir(produto_id, token)

    def test_atualizar_produto_sem_token_retorna_401(self, pclient, produto_cadastrado):
        # Arrange
        produto_id = produto_cadastrado["id"]
        payload_atualizado = {
            "nome": f"Produto Atualizado {uuid.uuid4().hex[:8]}",
            "preco": 200,
            "descricao": "Produto atualizado por teste automatizado",
            "quantidade": 20,
        }

        # Act
        resposta = pclient.atualizar(produto_id, payload_atualizado, token=None)

        # Assert
        assert resposta.status_code == 401

    def test_atualizar_produto_com_nome_duplicado_retorna_400(self, pclient, token):
        # Arrange 
        payload1 = payload_produto_valido()  
        payload2 = payload_produto_valido()  

        criacao1 = pclient.cadastrar(payload1, token)
        assert criacao1.status_code == 201
        produto_id1 = criacao1.json()["_id"]

        criacao2 = pclient.cadastrar(payload2, token)
        assert criacao2.status_code == 201
        produto_id2 = criacao2.json()["_id"]

      
        payload_duplicado = payload_produto_valido()
        payload_duplicado["nome"] = payload1["nome"]

        # Act
        resposta = pclient.atualizar(produto_id2, payload_duplicado, token)

        # Assert
        assert resposta.status_code == 400

        # Cleanup
        pclient.excluir(produto_id1, token)
        pclient.excluir(produto_id2, token)
    
    def test_atualizar_produto_com_token_nao_admin_retorna_403(self, pclient, produto_cadastrado, token_nao_admin):
        # Arrange
        payload = payload_produto_valido()
        # Act
        resposta = pclient.atualizar(produto_cadastrado["id"], payload, token_nao_admin)
        # Assert
        assert resposta.status_code == 403

   

@pytest.mark.produtos
class TestExcluirProduto:
    def test_excluir_produto_existente_retorna_200(self, pclient, produto_cadastrado, token):
        # Arrange
        produto_id = produto_cadastrado["id"]

        # Act
        resposta = pclient.excluir(produto_id, token)

        # Assert
        assert resposta.status_code == 200

    def test_excluir_produto_inexistente_retorna_400(self, pclient, token):
        # Arrange
        id_inexistente = "000000000000000000000000"

        # Act
        resposta = pclient.excluir(id_inexistente, token)

        # Assert
        assert resposta.status_code == 400

    def test_excluir_produto_sem_token_retorna_401(self, pclient, produto_cadastrado):
        # Arrange
        produto_id = produto_cadastrado["id"]

        # Act
        resposta = pclient.excluir(produto_id, token=None)

        # Assert
        assert resposta.status_code == 401

    def test_excluir_produto_com_token_nao_admin_retorna_403(self, pclient, produto_cadastrado, token_nao_admin):
        resposta = pclient.excluir(produto_cadastrado["id"], token_nao_admin)
        assert resposta.status_code == 403