.PHONY: venv install run gunicorn test

venv:
	python -m venv .venv

install: venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. .venv/bin/activate && FLASK_SECRET_KEY=$${FLASK_SECRET_KEY:-dev} PORT=$${PORT:-8000} HOST=$${HOST:-0.0.0.0} python app_server.py

gunicorn:
	. .venv/bin/activate && FLASK_SECRET_KEY=$${FLASK_SECRET_KEY:-dev} PORT=$${PORT:-8000} gunicorn app_server:app -b 0.0.0.0:$${PORT} --workers 2

test:
	. .venv/bin/activate || true; pip install -q pytest || true; pytest -q
