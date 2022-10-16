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
	TEST=true python -m uvicorn app.main:app --reload

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	PYTHONPATH=. venv/bin/pytest app/tests

docker/build:
	docker build -t myimage .

docker/run/develop:
	docker run --platform linux/amd64 -d -p 80:80 -v $(shell pwd)/app:/app myimage /start-reload.sh
