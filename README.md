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

## CI/CD

O projeto usa GitHub Actions para integração e entrega contínua, com três workflows em [`.github/workflows`](.github/workflows):

### Integração Contínua

| Workflow | Gatilho | O que faz |
|---|---|---|
| [`build.yml`](.github/workflows/build.yml) | Push em qualquer branch | Instala dependências com Poetry e roda a suíte de testes (`manage.py test`) |
| [`workflow-pr.yml`](.github/workflows/workflow-pr.yml) | Pull request | Roda testes e faz lint com o [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide), comentando o resultado direto no PR |

### Entrega Contínua — Deploy no Heroku

O workflow [`heroku-deploy.yml`](.github/workflows/heroku-deploy.yml) é disparado a cada push na branch `main` e publica a aplicação no Heroku automaticamente. Ele funciona em conjunto com o [`heroku.yml`](heroku.yml), que configura o app no **stack `container`**: em vez de usar buildpacks, o Heroku builda a imagem a partir do [`Dockerfile`](Dockerfile) do projeto e roda `gunicorn` como processo web.

Passo a passo do workflow:

1. **Checkout** do repositório com histórico completo (`fetch-depth: 0`), necessário para o `git push` no passo final.
2. **Instalação do Heroku CLI** no runner — o `ubuntu-latest` não vem mais com o CLI pré-instalado.
3. **Login no Heroku** via `~/.netrc`, usando as credenciais dos secrets.
4. **Adição do remote** `heroku`, apontando para o app configurado.
5. **Push para o Heroku** com `git push heroku HEAD:main`. Usar `HEAD` em vez de `main` é necessário porque o `actions/checkout` deixa o repositório em estado de *detached HEAD*, sem uma branch local chamada `main` para referenciar.

Ao receber o push, o Heroku detecta o `heroku.yml`, builda a imagem Docker e faz o release automaticamente — sem passos manuais.

#### Configurando os secrets

O workflow depende de três *repository secrets*, configurados em **Settings → Secrets and variables → Actions → Repository secrets**:

| Secret | Descrição |
|---|---|
| `HEROKU_API_KEY` | Token de API da conta Heroku (`heroku authorizations:create`) |
| `HEROKU_EMAIL` | E-mail da conta Heroku |
| `HEROKU_APP_NAME` | Nome do app já criado no Heroku |

Esses secrets ficam disponíveis apenas para os workflows do repositório — não devem ser confundidos com *environment secrets* (que exigem declarar `environment:` no job) nem com configurações de proteção de branch.

## Estrutura do projeto

```
bookstore/   # configurações do projeto (settings, urls, wsgi)
product/     # app de categorias e produtos
order/       # app de pedidos
```
