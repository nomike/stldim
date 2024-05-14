.PHONY: build clean upload-test

build:
	python3 -m build

clean:
	rm -rf dist

upload-test:
	python3 -m twine upload --repository testpypi dist/*
