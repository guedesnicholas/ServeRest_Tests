import pytest
from jsonschema import validate
from src.helpers.schemas import SCHEMA_LOGIN, SCHEMA_LOGIN_ERRADO


@pytest.mark.login
class Testlogins:
    def test_login_valido_retorna_200_token(self, client, usuario_cadastrado):

        # Arrange
        email = usuario_cadastrado["payload"]["email"]
        password = usuario_cadastrado["payload"]["password"]

        # Act
        resposta = client.login({
            "email": email,
            "password": password,
        })
        
        # Assert
        assert resposta.status_code == 200
        assert "authorization" in resposta.json()
        validate(instance=resposta.json(), schema=SCHEMA_LOGIN)  # Vai validar o json


    def test_login_email_inexistente_retorna_401(self, client, usuario_cadastrado):
        # Arrange
        email = "email.inexistente@qa.com"
        password = usuario_cadastrado["payload"]["password"]

        # Act
        resposta = client.login({
            "email": email,
            "password": password,
        })
        
        # Assert
        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Email e/ou senha inválidos"
        validate(instance=resposta.json(), schema=SCHEMA_LOGIN_ERRADO)  # Vai validar o json


    
    def test_login_senha_inexistente_retorna_401(self, client, usuario_cadastrado):
        # Arrange
        email = usuario_cadastrado["payload"]["email"]
        password = "senhadotantofaz123"

        # Act
        resposta = client.login({
            "email": email,
            "password": password,
        })
        
        # Assert
        assert resposta.status_code == 401
        assert resposta.json()["message"] == "Email e/ou senha inválidos"
        validate(instance=resposta.json(), schema=SCHEMA_LOGIN_ERRADO)  # Vai validar o json