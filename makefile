SHELL := /bin/bash

build: clean test_requirements

resin_cli:
	npm install --global --production resin-cli

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

run_on_rpi:
	./start.sh

test_requirements:
	pip install pip-tools
	pip-sync requirements/test.txt

update_requirements:
	pip-compile --output-file requirements/common.txt requirements/common.in
	pip-compile --output-file requirements/rpi.txt requirements/rpi.in
	pip-compile --output-file requirements/test.txt requirements/test.in

upgrade_requirements:
	pip-compile --upgrade --output-file requirements/common.txt requirements/common.in
	pip-compile --upgrade --output-file requirements/rpi.txt requirements/rpi.in
	pip-compile --upgrade --output-file requirements/test.txt requirements/test.in

# Set hashes according to resin.io app dashboard
resin_ssh_sense1:
	resin ssh $(CNAV_SENSE1_ID)
resin_ssh_sense2:
	resin ssh $(CNAV_SENSE2_ID)
resin_ssh_sense3:
	resin ssh $(CNAV_SENSE3_ID)

# Set addresses as env vars according to resin.io app dashboard
ssh_sense1:
	ssh root@$(CNAV_SENSE1_IP)
ssh_sense2:
	ssh root@$(CNAV_SENSE2_IP)
ssh_sense3:
	ssh root@$(CNAV_SENSE3_IP)

static_analysis: pep8 xenon

pep8:
	@echo "Running flake8 over codebase"
	flake8 --ignore=E501,W391,F999,E402 cnavsense/

xenon:
	@echo "Running xenon over codebase"
	xenon --max-absolute B --max-modules B --max-average A cnavsense/

test: static_analysis
	py.test -rw cnavsense --timeout=1 --cov=cnavsense $(pytest_args)

deploy:
	git push resin master

.PHONY: build clean test_requirements test static_analysis pep8 xenon run_on_rpi update_requirements upgrade_requirements deploy ssh_sense1 ssh_sense2 ssh_sense3 resin_ssh_sense1 resin_ssh_sense2 resin_ssh_sense3
