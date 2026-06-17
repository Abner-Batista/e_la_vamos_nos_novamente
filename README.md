# Sistema de Acervo — FastAPI + PostgreSQL + Docker

Este projeto consiste em um serviço web para gerenciar informações de livros de uma biblioteca (CRUD). O sistema foi construído sobre o ecossistema FastAPI e utiliza banco de dados PostgreSQL integrado por meio de containers Docker.

---

## Componentes Técnicos

- **FastAPI** — Criação da estrutura de endpoints
- **SQLAlchemy** — Mapeamento objeto-relacional
- **PostgreSQL** — Persistência relacional de dados
- **Docker & Compose** — Criação de ambiente isolado
- **Pytest** — Validação automatizada

---

## Requisitos do Sistema

- **Docker Engine** configurado
- **Docker Compose** utilitário ativo

---

## Iniciando a Aplicação

1. Obtenha os arquivos locais:
   ```bash
   git clone <link-do-repositorio>
   cd trabalho_faculdade
   ```

2. Construa e inicie os containers:
   ```bash
   docker compose up --build
   ```

3. Acesse a API em funcionamento em: [http://localhost:8000](http://localhost:8000)

4. A interface de documentação interativa (Swagger UI) está acessível em: [http://localhost:8000/docs](http://localhost:8000/docs)

5. Para finalizar a execução dos containers:
   ```bash
   docker compose down
   ```

---

## Endpoints Criados

| Método | Caminho | Objetivo |
|--------|---------|----------|
| GET | `/livros` | Lista todos os livros do acervo |
| POST | `/livros` | Cadastra um novo livro |
| GET | `/livros/{livro_id}` | Obtém os dados de um livro específico |
| PUT | `/livros/{livro_id}` | Altera as informações de um livro |
| DELETE | `/livros/{livro_id}` | Exclui um livro do acervo |

### Estrutura de dados para cadastro (POST / PUT):

```json
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "paginas": 256,
  "disponivel": true
}
```

---

## Rodando os Testes do Sistema

1. Prepare e inicie um ambiente virtual do Python:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Efetue a instalação das dependências obrigatórias:
   ```bash
   pip install -r requirements.txt
   ```

3. Rode a bateria de validações:
   ```bash
   pytest
   ```

4. Para checar a cobertura de testes:
   ```bash
   pytest --cov=app
   ```

> Nota: A suíte de testes utiliza um banco de dados SQLite volátil em memória, eliminando a necessidade de containers ativos durante os testes.

---

## Disposição dos Arquivos do Projeto

```
trabalho_faculdade/
├── app/
│   ├── __init__.py
│   ├── main.py        # definição de endpoints e lógica
│   ├── database.py    # conexão e sessões do SQLAlchemy
│   ├── models.py      # estruturas das tabelas SQL
│   └── schemas.py     # formatos de dados do Pydantic
├── tests/
│   ├── conftest.py    # fixtures gerais de teste
│   └── test_livros.py # validação das rotas do acervo
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Resultado da Validação do Acervo

Abaixo está o registro da execução com sucesso das rotas:

```text
============================= test session starts ==============================
platform win32 -- Python 3.12.2, pytest-8.1.1, pluggy-1.4.0 -- C:\Users\usuario\trabalho_faculdade\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\usuario\trabalho_faculdade
plugins: anyio-4.3.0, cov-5.0.0
collecting ... collected 10 items                                                             

tests/test_livros.py::test_obter_acervo_vazio PASSED                     [ 10%]
tests/test_livros.py::test_cadastrar_livro PASSED                        [ 20%]
tests/test_livros.py::test_cadastrar_livro_padrao_disponivel PASSED      [ 30%]
tests/test_livros.py::test_listar_acervo_com_livros PASSED               [ 40%]
tests/test_livros.py::test_localizar_livro_id PASSED                     [ 50%]
tests/test_livros.py::test_localizar_livro_inexistente PASSED            [ 60%]
tests/test_livros.py::test_modificar_livro PASSED                        [ 70%]
tests/test_livros.py::test_modificar_livro_inexistente PASSED            [ 80%]
tests/test_livros.py::test_remover_livro PASSED                          [ 90%]
tests/test_livros.py::test_remover_livro_inexistente PASSED              [100%]

============================== 10 passed in 1.10s ==============================
```
