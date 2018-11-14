.PHONY: build

build:
	python3.5 setup.py sdist bdist_wheel

clean:
	rm -rf dist build
