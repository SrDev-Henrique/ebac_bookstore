# Set this to ~use it everywhere in the project setup
PYTHON_VERSION ?= 3.13

POETRY_OPTS ?=
POETRY ?= poetry $(POETRY_OPTS)
RUN_PYPKG_BIN = $(POETRY) run

# Docker Compose binary, override with `make <target> COMPOSE="docker-compose"` if you're on v1
COMPOSE ?= docker compose

COLOR_ORANGE = \033[33m
COLOR_RESET = \033[0m

##@ Utility

.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: version-python
version-python: ## Echos the version of Python in use
	@echo $(PYTHON_VERSION)

##@ Setup

.PHONY: deps
deps: ## Installs Python dependencies with Poetry
	$(POETRY) install

##@ Testing

.PHONY: test
test: ## Runs the Django test suite
	$(RUN_PYPKG_BIN) python manage.py test

##@ Code Quality

.PHONY: check
check: ## Runs basedpyright type checking
	$(RUN_PYPKG_BIN) basedpyright

##@ Docker

.PHONY: up
up: ## Starts the app and database containers
	$(COMPOSE) up -d

.PHONY: up-build
up-build: ## Rebuilds images and starts the containers
	$(COMPOSE) up -d --build

.PHONY: down
down: ## Stops and removes the containers
	$(COMPOSE) down

.PHONY: logs
logs: ## Follows the web container logs
	$(COMPOSE) logs -f web

.PHONY: migrate
migrate: ## Applies database migrations inside the web container
	$(COMPOSE) exec web python manage.py migrate --noinput

.PHONY: makemigrations
makemigrations: ## Generates new migrations inside the web container
	$(COMPOSE) exec web python manage.py makemigrations

.PHONY: superuser
superuser: ## Creates a Django superuser inside the web container
	$(COMPOSE) exec web python manage.py createsuperuser

.PHONY: shell
shell: ## Opens a Django shell inside the web container
	$(COMPOSE) exec web python manage.py shell
