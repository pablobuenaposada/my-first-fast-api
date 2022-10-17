DOCKER_IMAGE=fast-api

venv:
	python3.9 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black app
	venv/bin/isort app

format/check: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose app --check
	venv/bin/isort --df -c app

run/local: venv
	TEST=true venv/bin/uvicorn app.main:app --reload

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	DATABASE=sqlite:///./test.db PYTHONPATH=app venv/bin/pytest app/tests

docker/build:
	docker build -t $(DOCKER_IMAGE) .

docker/run/develop:
	docker run --platform linux/amd64 -d -p 80:80 -v $(shell pwd)/app:/app $(DOCKER_IMAGE) /start-reload.sh

docker/run:
	docker run --env TEST=true --platform linux/amd64 -d --name $(DOCKER_IMAGE) -p 80:80 $(DOCKER_IMAGE)
