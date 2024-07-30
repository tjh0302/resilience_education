default:
	@cat makefile

env:
	python3 -m venv env; source env/bin/activate ; pip install --upgrade pip

update: env
	source env/bin/activate && pip install -r requirements.txt 

jupyterlab: update
	source env/bin/activate ; jupyter lab

test: update
	source env/bin/activate && PYTHONPATH=/Users/zsk4gm/Desktop/resilience_education pytest

run: update
	source env/bin/activate && PYTHONWARNINGS="ignore" python3 rag_executable.py
