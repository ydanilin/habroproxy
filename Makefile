install:
	pip install -r requirements.txt
lint:
	pylint ./habroproxy
test:
	pytest --ignore=habroproxy/test/test_tls.py
fulltest:
	pytest
run:
	python run.py
gencert:
	python habroproxy/tools/gencert.py
