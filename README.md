# ServeRest — Testes Automatizados: Usuários

Suíte de testes para o endpoint `/usuarios` e `/login` da [ServeRest](https://compassuol.serverest.dev/).

## Estrutura do projeto

```
.
├── src/
│   ├── api/
│   │   └── usuarios_client.py   # Cliente HTTP para o endpoint
│   └── helpers/
│       └── factories.py         # Geração de dados dinâmicos
├── tests/
│   ├── conftest.py              # Fixtures globais (com cleanup via yield)
│   └── test_usuarios.py        # 13 cenários de teste
├── pytest.ini
└── requirements.txt
```

## Pré-requisitos

- Python 3.10+
- pip

## Como rodar

```bash

# 1. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute os testes
pytest

# Rodar apenas os testes de usuários
pytest -m usuarios

# Rodar um teste por vez
pytest -k "nome_da_função" 

# Ver output detalhado
pytest -v
```

## Cenários cobertos

| # | Cenário | Método |
|---|---------|--------|
| 1 | Listar usuários retorna 200 e estrutura correta | GET /usuarios |
| 2 | Cadastrar usuário válido retorna 201 com `_id` | POST /usuarios |
| 3 | Cadastrar com email duplicado retorna 400 | POST /usuarios |
| 4 | Cadastrar sem nome retorna 400 | POST /usuarios |
| 5 | Cadastrar sem email retorna 400 | POST /usuarios |
| 6 | Cadastrar sem password retorna 400 | POST /usuarios |
| 7 | Buscar por ID existente retorna 200 com dados corretos | GET /usuarios/:id |
| 8 | Buscar por ID inexistente retorna 400 | GET /usuarios/:id |
| 9 | Atualizar usuário existente retorna 200 | PUT /usuarios/:id |
| 10 | Atualizar ID inexistente cria novo usuário (upsert) | PUT /usuarios/:id |
| 11 | Atualizar usuário com email que já está cadastrado 400 | PUT /usuarios/:id |
| 12 | Excluir usuário existente retorna 200 | DELETE /usuarios/:id |
| 13 | Excluir ID inexistente retorna 200 sem exclusão | DELETE /usuarios/:id |

