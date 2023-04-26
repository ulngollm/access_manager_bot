install:
	pip install -r requirements.txt
venv-start:
	source venv/bin/activate
venv-stop:
	deactivate
venv-install:
	python3 -m venv venv
