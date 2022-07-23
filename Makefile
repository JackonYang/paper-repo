PY?=python3
PIP?=pip3
DC?=docker-compose

CODE_ROOT?=code

check-dup:
	cd code && python manage.py check-dup

clean-deleted:
	cd $(CODE_ROOT) && bash scripts/clean_deleted_data.sh

gen-meta:
	cd code && python manage.py gen-meta

gen-readme:
	cd code && python manage.py update-readme

gen-notes-md:
	cd code && python manage.py gen-notes-md

dvc-add:
	git status -s | rev | awk '{print $1}' | rev | xargs -I{} dvc add {}

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

.PHONY: check-dup gen-meta gen-readme gen-notes-md
.PHONY: clean-deleted
.PHONY: dvc-add push-all
.PHONY: setup flake8 test
