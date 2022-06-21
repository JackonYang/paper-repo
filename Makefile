PY?=python3
PIP?=pip3
DC?=docker-compose

CODE_ROOT?=code

check-dup:
	cd code && python manage.py check-dup

gen-meta:
	cd code && python manage.py gen-meta

update-readme:
	cd code && python manage.py update-readme

gen-md-notes:
	cd code && python manage.py gen-md-notes

dvc-add:
	dvc add pdfs/*.pdf
	make gen-meta
	make check-dup

push-all:
	make flake8
	dvc push
	git push

setup:
	bash $(CODE_ROOT)/scripts/set-env-mac.sh

flake8:
	flake8 $(CODE_ROOT)

test:
	PYTHONPATH=$(CODE_ROOT) pytest --cov $(CODE_ROOT) --cov-report term-missing:skip-covered --capture=no -p no:cacheprovider

.PHONY: check-dup gen-meta update-readme gen-md-notes
.PHONY: dvc-add
.PHONY: setup flake8 ut
