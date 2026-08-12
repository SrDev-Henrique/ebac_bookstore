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
| `CSRF_TRUSTED_ORIGINS` | Origens HTTPS confiáveis (ex.: `https://seu-app.onrender.com`) | vazio |
| `SQL_ENGINE` | Backend do banco | `django.db.backends.sqlite3` |
| `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT` | Credenciais do Postgres (usadas via Docker) | — |

Sem essas variáveis definidas, o projeto roda normalmente com SQLite.

## Deploy no Render

1. Crie um **PostgreSQL** e um **Web Service** (Python 3) no mesmo region.
2. Configure o serviço com:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn bookstore.wsgi:application`
3. Defina as variáveis de ambiente no Web Service:

| Variável | Valor |
|---|---|
| `SECRET_KEY` | Generate no painel do Render |
| `DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `seu-app.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://seu-app.onrender.com` |
| `SQL_ENGINE` | `django.db.backends.postgresql` |
| `SQL_DATABASE` / `SQL_USER` / `SQL_PASSWORD` / `SQL_HOST` / `SQL_PORT` | Dados do Postgres no Render (use o host **Internal**) |

O arquivo [`.python-version`](.python-version) fixa Python 3.13. O [`build.sh`](build.sh) instala as dependências com Poetry, roda `collectstatic` e aplica as migrations.

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
| Cadastro de usuário | `/bookstore/v1/users/` (`POST`) |
| Admin | `/admin/` |
| Autenticação por token | `/api-token-auth/` |

Todas as rotas de recursos são públicas (`AllowAny`) — não exigem autenticação. O cadastro de usuário aceita `username`, `email` e `password` via `POST` e não lista usuários (`GET` retorna 405). Basic, Session e Token continuam disponíveis se você quiser usá-los; `/api-token-auth/` ainda gera token a partir de usuário e senha.

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
