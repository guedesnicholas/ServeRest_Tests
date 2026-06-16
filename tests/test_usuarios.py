import pytest
from src.helpers.factories import payload_usuario_valido


# Arrange = Monta o payload, pega dados da fixture
# Act = Chama o método do client
# Assert = Verifica status code + corpo da resposta


@pytest.mark.usuarios
class TestListarUsuarios:
    def test_listar_usuarios_retorna_200_e_lista(self, client):
        # Arrange + Act
        resposta = client.listar()

        # Assert
        assert resposta.status_code == 200
        corpo = resposta.json()
        assert "quantidade" in corpo
        assert "usuarios" in corpo
        assert isinstance(corpo["usuarios"], list)


@pytest.mark.usuarios
class TestCadastrarUsuario:
    def test_cadastrar_usuario_valido_retorna_201_com_id(self, client, usuario_cadastrado):
        # Arrange — usuário já criado pela fixture

        # Act — buscamos ele pelo ID para confirmar que existe
        resposta = client.buscar_por_id(usuario_cadastrado["id"])

        # Assert
        assert resposta.status_code == 200
        assert "_id" in resposta.json()

    def test_cadastrar_usuario_com_email_duplicado_retorna_400(self, client, usuario_cadastrado):
        # Arrange — reutiliza o email já cadastrado pela fixture
        payload = payload_usuario_valido()
        payload["email"] = usuario_cadastrado["payload"]["email"]

        # Act
        resposta = client.cadastrar(payload)

        # Assert
        assert resposta.status_code == 400
        assert "Este email já está sendo usado" in resposta.json()["message"]

    def test_cadastrar_usuario_sem_nome_retorna_400(self, client):
        # Arrange
        payload = payload_usuario_valido()
        del payload["nome"]

        # Act
        resposta = client.cadastrar(payload)

        # Assert
        assert resposta.status_code == 400
        assert "nome" in resposta.json()

    def test_cadastrar_usuario_sem_email_retorna_400(self, client):
        # Arrange
        payload = payload_usuario_valido()
        del payload["email"]

        # Act
        resposta = client.cadastrar(payload)

        # Assert
        assert resposta.status_code == 400
        assert "email" in resposta.json()

    def test_cadastrar_usuario_sem_password_retorna_400(self, client):
        # Arrange
        payload = payload_usuario_valido()
        del payload["password"]

        # Act
        resposta = client.cadastrar(payload)

        # Assert
        assert resposta.status_code == 400
        assert "password" in resposta.json()


@pytest.mark.usuarios
class TestBuscarUsuarioPorId:
    def test_buscar_usuario_existente_retorna_200_com_dados_corretos(self, client, usuario_cadastrado):
        # Arrange
        usuario_id = usuario_cadastrado["id"]

        # Act
        resposta = client.buscar_por_id(usuario_id)

        # Assert
        assert resposta.status_code == 200
        corpo = resposta.json()
        assert corpo["_id"] == usuario_id
        assert corpo["nome"] == usuario_cadastrado["payload"]["nome"]
        assert corpo["email"] == usuario_cadastrado["payload"]["email"]

    def test_buscar_usuario_inexistente_retorna_400(self, client):
        # Arrange
        id_inexistente = "000000000000000000000000"

        # Act
        resposta = client.buscar_por_id(id_inexistente)

        # Assert — validamos apenas o status code, que é o contrato garantido
        assert resposta.status_code == 400


@pytest.mark.usuarios
class TestAtualizarUsuario:
    def test_atualizar_usuario_existente_retorna_200(self, client, usuario_cadastrado):
        # Arrange
        usuario_id = usuario_cadastrado["id"]
        payload_atualizado = {
            "nome": "Nome Atualizado",
            "email": "email.atualizado@qa.com",
            "password": "novaSenha456",
            "administrador": "false",
        }

        # Act
        resposta = client.atualizar(usuario_id, payload_atualizado)

        # Assert
        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro alterado com sucesso"

    def test_atualizar_usuario_inexistente_cria_novo_usuario(self, client):
        # Arrange
        id_inexistente = "aaaaaaaaaaaaaaaaaaaaaaaa"
        payload = {
            "nome": "Usuario Upsert",
            "email": "upsert.teste@qa.com",
            "password": "senha123",
            "administrador": "false",
        }

        # Act
        resposta = client.atualizar(id_inexistente, payload)

        # Assert: ServeRest cria o registro quando o ID não existe (upsert)
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert "message" in corpo

        # Cleanup
        novo_id = corpo.get("_id")
        if novo_id:
            client.excluir(novo_id)
    
    def test_atualizar_usuario_com_email_ja_usado_retorna_400(self, client):
        # Arrange — cria dois usuários
        payload1 = payload_usuario_valido()
        payload2 = payload_usuario_valido()

        criacao1 = client.cadastrar(payload1)
        assert criacao1.status_code == 201
        usuario_id1 = criacao1.json()["_id"]

        criacao2 = client.cadastrar(payload2)
        assert criacao2.status_code == 201
        usuario_id2 = criacao2.json()["_id"]

        # tenta atualizar usuario2 com o email do usuario1
        payload_atualizado = payload_usuario_valido()
        payload_atualizado["email"] = payload1["email"]

        # Act
        resposta = client.atualizar(usuario_id2, payload_atualizado)

        # Assert
        assert resposta.status_code == 400

        # Cleanup
        client.excluir(usuario_id1)
        client.excluir(usuario_id2)



@pytest.mark.usuarios
class TestExcluirUsuario:
    def test_excluir_usuario_existente_retorna_200(self, client, usuario_cadastrado):
        # Arrange — usuário já existe via fixture
        usuario_id = usuario_cadastrado["id"]

        # Act
        resposta = client.excluir(usuario_id)

        # Assert
        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Registro excluído com sucesso"

    def test_excluir_usuario_inexistente_retorna_200_sem_exclusao(self, client):
        # Arrange
        id_inexistente = "000000000000000000000000"

        # Act
        resposta = client.excluir(id_inexistente)

        # Assert
        assert resposta.status_code == 200
        assert resposta.json()["message"] == "Nenhum registro excluído"