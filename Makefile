
clean:
	find . -name '*.pyc' -exec rm '{}' ';'
	find . -name '__pycache__' -type d -prune -exec rm -rf '{}' '+'
	find . -name '.pytest_cache' -type d -prune -exec rm -rf '{}' '+'

test: clean
	./run-tests.sh

run:
	flask run --host=0.0.0.0

format:
	black eventsync tests
	isort -rc eventsync tests