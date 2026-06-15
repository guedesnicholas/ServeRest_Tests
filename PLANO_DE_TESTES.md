# Plano de Testes — ServeRest API

## Objetivo

Validar o comportamento dos endpoints `/usuarios` e `/login` da ServeRest
garantindo que todas as operações funcionam conforme esperado, retornam os status codes
corretos e respeitam as regras de negócio da API.

---

## Estratégia

| Item | Decisão |
|---|---|
| Tipo de teste | Testes de API (integração) |
| Camada | HTTP direto, sem UI |
| Ferramentas | Python 3.12, Pytest, Requests |
| Ambiente | https://compassuol.serverest.dev |
| Padrão de teste | AAA — Arrange, Act, Assert |
| Isolamento | Email dinâmico com uuid por execução |
| Cleanup | Fixtures com yield + cleanup manual nos testes autossuficientes |
| Autenticação | Token obtido via POST /login, escopo de sessão |

---

## Escopo

### Coberto
- Listar, cadastrar, buscar, atualizar e excluir usuários
- Autenticação via login com credenciais válidas e inválidas

### Fora do escopo
- Endpoint de produtos (`/produtos`)
- Endpoint de carrinhos (`/carrinhos`)
- Testes de carga e performance
- Testes de contrato (schema validation)

---

## Cenários por Endpoint

### GET /usuarios
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 01 | Listar todos os usuários | 200 | ✅ |

### POST /usuarios
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 02 | Cadastrar usuário com dados válidos | 201 | ✅ |
| 03 | Cadastrar com email duplicado | 400 | ✅ |
| 04 | Cadastrar sem campo nome | 400 | ✅ |
| 05 | Cadastrar sem campo email | 400 | ✅ |
| 06 | Cadastrar sem campo password | 400 | ✅ |

### GET /usuarios/:id
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 07 | Buscar usuário com ID existente | 200 | ✅ |
| 08 | Buscar usuário com ID inexistente | 400 | ✅ |

### PUT /usuarios/:id
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 09 | Atualizar usuário existente | 200 | ✅ |
| 10 | Atualizar ID inexistente cria novo usuário (upsert) | 201 | ✅ |
| 11 | Atualizar com email já usado por outro usuário | 400 | ⬜ |

### DELETE /usuarios/:id
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 12 | Excluir usuário existente | 200 | ✅ |
| 13 | Excluir usuário inexistente | 200 | ✅ |


---

### POST /login
| # | Cenário | Status Esperado | Implementado |
|---|---|---|---|
| 14 | Login com credenciais válidas retorna token | 200 | ✅ |
| 15 | Login com email inexistente | 401 | ✅ |
| 16 | Login com password incorreto | 401 | ✅ |

---

## Critérios de Qualidade

Um teste está pronto quando:

- [ ] Nome segue o padrão `test_acao_condicao_resultado_esperado`
- [ ] Segue o padrão AAA com comentários `# Arrange`, `# Act`, `# Assert`
- [ ] Roda isolado sem depender de outro teste
- [ ] Faz cleanup dos dados que criou
- [ ] Valida o status code da resposta
---


## Legenda

- ✅ Implementado
- ⬜ Não implementado