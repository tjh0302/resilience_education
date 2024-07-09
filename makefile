default:
	@cat makefile

env:
	python3 -m venv env; source env/bin/activate ; pip install --upgrade pip

update: env
	source env/bin/activate; pip install -r requirements.txt

jupyterlab: update
	source env/bin/activate ; jupyter lab
