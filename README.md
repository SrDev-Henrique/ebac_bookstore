# BookStore API

API REST para uma livraria, construída com Django e Django REST Framework como parte do curso de Backend da EBAC.

## Stack

- Python 3.13
- Django 6.0
- Django REST Framework
- PostgreSQL (Docker) / SQLite (dev local sem Docker)
- Poetry para gerenciamento de dependências
- Docker + Docker Compose

## Requisitos

- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) e Docker Compose (para rodar com Postgres)
- `make` (opcional, mas recomendado — veja os atalhos abaixo)

## Configuração

Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

As variáveis usadas são:

| Variável | Descrição | Padrão (local, sem Docker) |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | chave de desenvolvimento embutida |
| `DEBUG` | Ativa modo debug (`1`/`0`) | `1` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por espaço | `localhost 127.0.0.1` |
| `SQL_ENGINE` | Backend do banco | `django.db.backends.sqlite3` |
| `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT` | Credenciais do Postgres (usadas via Docker) | — |

Sem essas variáveis definidas, o projeto roda normalmente com SQLite.

## Rodando com Docker (recomendado)

```bash
make up-build   # ou: docker compose up -d --build
```

Isso sobe dois containers:

- `web`: aplicação Django, aplica as migrations automaticamente e roda em `http://localhost:8000`
- `db`: PostgreSQL 16, com healthcheck e volume persistente

## Rodando localmente sem Docker

```bash
make deps                        # ou: poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Comandos úteis (Makefile)

Rode `make help` para ver todos os comandos disponíveis:

| Comando | Descrição |
|---|---|
| `make deps` | Instala as dependências com Poetry |
| `make test` | Roda a suíte de testes (`manage.py test`) |
| `make check` | Roda o type checking com basedpyright |
| `make up` | Sobe os containers |
| `make up-build` | Reconstrói as imagens e sobe os containers |
| `make down` | Para e remove os containers |
| `make logs` | Acompanha os logs do container `web` |
| `make migrate` | Aplica as migrations dentro do container `web` |
| `make makemigrations` | Gera novas migrations dentro do container `web` |
| `make superuser` | Cria um superusuário dentro do container `web` |
| `make shell` | Abre o shell do Django dentro do container `web` |

## Endpoints

Todas as rotas da API ficam sob `/bookstore/<versão>/`, onde `<versão>` é `v1` ou `v2`.

| Recurso | Rota |
|---|---|
| Categorias | `/bookstore/v1/categories/` |
| Produtos | `/bookstore/v1/products/` |
| Pedidos | `/bookstore/v1/orders/` |
| Admin | `/admin/` |
| Autenticação por token | `/api-token-auth/` |

Todas as rotas de recursos exigem autenticação (Basic, Session ou Token). Use `/api-token-auth/` para obter um token a partir de usuário e senha.

## Testes

```bash
make test
```

## Estrutura do projeto

```
bookstore/   # configurações do projeto (settings, urls, wsgi)
product/     # app de categorias e produtos
order/       # app de pedidos
```
