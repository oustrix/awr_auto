run:
	python start.py

deps:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

lint:
	black .

build:
	pyinstaller start.py