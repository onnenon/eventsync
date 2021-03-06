
clean:
	find . -name '*.pyc' -exec rm '{}' ';'
	find . -name '__pycache__' -type d -prune -exec rm -rf '{}' '+'
	find . -name '.pytest_cache' -type d -prune -exec rm -rf '{}' '+'

test:
	coverage run --source=eventsync -m pytest -p no:warnings -v
	coverage report
	coverage html

run:
	cd eventsync && flask run --host=0.0.0.0

format:
	black eventsync tests
	isort -rc eventsync tests

db-up:
	cd vagrant && vagrant up

db-reset:
	cd vagrant && \
	vagrant destroy -f eventsync-db && vagrant up

db-destroy:
	cd vagrant && \
	vagrant destroy -f eventsync-db

