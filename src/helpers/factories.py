import uuid


def payload_usuario_valido(admin=False):
    #Retorna payload completo e válido para cadastro de usuário.
    return {
        "nome": "Usuario Teste Automatizado",
        "email": f"usuario_{uuid.uuid4().hex[:8]}@qa.com",
        "password": "senha123",
        "administrador": "true" if admin else "false",
    }




def payload_produto_valido():
    #Retorna payload completo e válido para cadastro de produtos.
    return {
        "nome": f"Produto Teste {uuid.uuid4().hex[:8]}",
        "preco": 100,
        "descricao": "Produto criado por teste automatizado",
        "quantidade": 10,
    }