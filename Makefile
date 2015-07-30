.PHONY: env help

all: help

env:
	if [ ! -d ".env" ]; then virtualenv -p /usr/bin/python2 .env; fi
	. .env/bin/activate; pip install -r requirements.txt

help: env
	@echo
	@echo "Use this to activate virtual environment:"
	@echo "    source .env/bin/activate"
	@echo
