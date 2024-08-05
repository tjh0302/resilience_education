default:
	@cat makefile

env:
	python3 -m venv env; source env/bin/activate ; pip install --upgrade pip

update: env
	source env/bin/activate && pip install -r requirements.txt 

develop: env
	source env/bin/activate && pip install -r requirements-dev.txt

jupyterlab: develop
	source env/bin/activate ; jupyter lab

PYTHONPATH := $(CURDIR)
test: update
	source env/bin/activate && PYTHONPATH=$(PYTHONPATH) pytest

run: update
	source env/bin/activate && PYTHONWARNINGS="ignore" python3 rag_executable.py
