TEST_PATH=./tests
RECIPEPREFIX= # prefix char is a space, on purpose; do not delete
PHONY=clean

clean: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name 'test_app.py' -exec rm -f {} +
	find . -name 'testbed_transforms.py' -exec rm -f {} +

install-deps:
	pipenv install
	pipenv install -e .

test:	clean
	pipenv run python -m unittest discover -s . ./tests -v

