SCHEMA_USUARIO = {
    "type": "object",
    "required": ["_id", "nome", "email", "password", "administrador"],
    "properties": {
        "_id":           {"type": "string"},
        "nome":          {"type": "string"},
        "email":         {"type": "string"},
        "password":      {"type": "string"},
        "administrador": {"type": "string", "enum": ["true", "false"]},
    }
}

SCHEMA_LISTA_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios":   {"type": "array", "items": SCHEMA_USUARIO},
    }
}

SCHEMA_USUARIO_ERRADO = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message":       {"type": "string"},
    }
}

SCHEMA_PRODUTO_ERRADO = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message":       {"type": "string"},
    }
}


SCHEMA_LOGIN = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message":       {"type": "string"},
        "authorization": {"type": "string"},
    }
}

SCHEMA_LOGIN_ERRADO = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message":       {"type": "string"},
    }
}


SCHEMA_PRODUTO = {
    "type": "object",
    "required": ["_id", "nome", "preco", "descricao", "quantidade"],
    "properties": {
        "_id":       {"type": "string"},
        "nome":      {"type": "string"},
        "preco":     {"type": "number"},
        "descricao": {"type": "string"},
        "quantidade":{"type": "integer"},
    }
}

SCHEMA_LISTA_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos":   {"type": "array", "items": SCHEMA_PRODUTO},
    }
}