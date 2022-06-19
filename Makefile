PY?=python3
PIP?=pip3
DC?=docker-compose

CODE_ROOT?=code

run_pipeline:
	cd code && python manage.py

dvc-add:
	dvc add pdfs/*.pdf

setup:
	bash $(CODE_ROOT)/scripts/set-env-mac.sh

flake8:
	flake8 $(CODE_ROOT)

test:
	PYTHONPATH=$(CODE_ROOT) pytest --cov $(CODE_ROOT) --cov-report term-missing:skip-covered --capture=no -p no:cacheprovider

.PHONY: pdf_pipeline
.PHONY: dvc-add
.PHONY: setup flake8 ut
