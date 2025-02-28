# Configurações
IMAGE_NAME=flask-gunicorn-app
PORT ?= 5000
ENV_FILE=.env
VENV=.venv

requirements:
	@pip freeze > requirements.txt

venv:
	@python3.11 -m venv $(VENV)
	@/bin/zsh -i -c "source $(VENV)/bin/activate"

install:
	@$(VENV)/bin/pip install -r requirements.txt

wsgi:
	@$(VENV)/bin/gunicorn wsgi:app --bind 0.0.0.0:$(PORT)

weaviate:
	@docker run -d \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=20 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  --name weaviate \
  semitechnologies/weaviate:latest