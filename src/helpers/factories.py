import uuid


def payload_usuario_valido(admin=False):
    #Retorna payload completo e válido para cadastro de usuário.
    return {
        "nome": "Usuario Teste Automatizado",
        "email": f"usuario_{uuid.uuid4().hex[:8]}@qa.com",
        "password": "senha123",
        "administrador": "true" if admin else "false",
    }
