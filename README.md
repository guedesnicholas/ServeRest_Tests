# ServeRest — Testes Automatizados: Usuários

Suíte de testes para o endpoint `/usuarios` , `/login` e `/produtos` da [ServeRest](https://compassuol.serverest.dev/).

## Estrutura do projeto

```
.
├── src/
│   ├── api/
│   │   └── usuarios_client.py   # Cliente HTTP para o endpoint
│   └── helpers/
│       |── factories.py         # Geração de dados dinâmicos
|       └── schemas.py
├── tests/
│   ├── conftest.py              # Fixtures globais (com cleanup via yield)
│   |── test_usuarios.py         # 13 cenários de teste
│   |── test_login.py            #  3 cenários de teste
│   └── test_produtos.py         # 19 cenários de teste
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
| 10 | Atualizar ID inexistente cria novo usuário 201 | PUT /usuarios/:id |
| 11 | Atualizar usuário com email que já está cadastrado 400 | PUT /usuarios/:id |
| 12 | Excluir usuário existente retorna 200 | DELETE /usuarios/:id |
| 13 | Excluir ID inexistente retorna 200 sem exclusão | DELETE /usuarios/:id |
| 14 | Login com credenciais válidas retorna 200 e token | POST /login |
| 15 | Login com email inexistente retorna 401 | POST /login |
| 16 | Login com password incorreto retorna 401 | POST /login |
| 17 | Listar produtos retorna 200 e estrutura correta | GET /produtos |
| 18 | Cadastrar produto válido retorna 201 com `_id` | POST /produtos |
| 19 | Cadastrar produto sem token retorna 401 | POST /produtos |
| 20 | Cadastrar produto com token não admin retorna 403 | POST /produtos |
| 21 | Cadastrar produto com nome duplicado retorna 400 | POST /produtos |
| 22 | Cadastrar produto sem nome retorna 400 | POST /produtos |
| 23 | Cadastrar produto sem preco retorna 400 | POST /produtos |
| 24 | Cadastrar produto sem descricao retorna 400 | POST /produtos |
| 25 | Cadastrar produto sem quantidade retorna 400 | POST /produtos |
| 26 | Buscar produto por ID existente retorna 200 | GET /produtos/:id |
| 27 | Buscar produto por ID inexistente retorna 400 | GET /produtos/:id |
| 28 | Atualizar produto existente retorna 200 | PUT /produtos/:id |
| 29 | Atualizar produto sem token retorna 401 | PUT /produtos/:id |
| 30 | Atualizar produto com token não admin retorna 403 | PUT /produtos/:id |
| 31 | Atualizar produto com nome duplicado retorna 400 | PUT /produtos/:id |
| 32 | Excluir produto existente retorna 200 | DELETE /produtos/:id |
| 33 | Excluir produto inexistente retorna 400 | DELETE /produtos/:id |
| 34 | Excluir produto sem token retorna 401 | DELETE /produtos/:id |
| 35 | Excluir produto com token não admin retorna 403 | DELETE /produtos/:id |



## Cobertura de Testes

Método utilizado: **Status Code Coverage (Output)**

Todos os status codes documentados pela ServeRest foram exercitados
pelos testes para cada endpoint coberto.

| Endpoint | Status Codes Documentados | Cobertos | Cobertura |
|---|---|---|---|
| POST /usuarios | 201, 400 | 201, 400 | 100% |
| GET /usuarios/:id | 200, 400 | 200, 400 | 100% |
| PUT /usuarios/:id | 200, 201, 400 | 200, 201, 400 | 100% |
| DELETE /usuarios/:id | 200 | 200 | 100% |
| POST /login | 200, 401 | 200, 401 | 100% |
| POST /produtos | 201, 400, 401, 403 | 201, 400, 401, 403 | 100% |
| GET /produtos/:id | 200, 400 | 200, 400 | 100% |
| PUT /produtos/:id | 200, 400, 401, 403 | 200, 400, 401, 403 | 100% |
| DELETE /produtos/:id | 200, 400, 401, 403 | 200, 400, 401, 403 | 100% |
| **Total** | **todos** | **todos** | **100%** |


## Validação de Contrato

Foram implementadas validações de contrato utilizando JSON Schema para garantir que as respostas da API mantenham a estrutura esperada.

Endpoints cobertos:
- POST /usuarios
- POST /login
- POST /produtos
- GET /produtos/{id}


## Cenários fora do escopo

### /carrinhos
O endpoint de carrinhos não foi coberto nesta suíte pois não
estava previsto a cobertura.

### Validações de boundary em /usuarios
| Cenário | Motivo |
|---|---|
| Email com formato inválido | Fora do escopo mínimo definido |
| Password vazio | Fora do escopo mínimo definido |

### Validações de boundary em /produtos
| Cenário | Motivo |
|---|---|
| Preco negativo | Fora do escopo mínimo definido |
| Preco zero | Fora do escopo mínimo definido |
| Quantidade negativa | Fora do escopo mínimo definido |
| Quantidade zero | Fora do escopo mínimo definido |

### Testes de performance e carga
Não foram realizados testes de carga ou stress. A ServeRest é um
ambiente público compartilhado — testes de carga poderiam impactar
outros usuários da plataforma.

### Cenário: Excluir usuário com carrinho ativo
A ServeRest retorna 400 ao tentar excluir um usuário que possui
carrinho ativo. Este cenário não foi coberto pois exigiria interação
com o endpoint /carrinhos, que está fora do escopo desta suíte.

### Cenário: Excluir produto com carrinho ativo
Mesmo motivo do cenário anterior — exigiria interação com /carrinhos.