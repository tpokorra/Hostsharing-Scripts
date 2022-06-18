VENV := . .venv/bin/activate &&

all:
	@echo "help:"
	@echo "  make quickstart"

quickstart: create_venv pip_packages

pip_packages:
	${VENV} pip3 install --upgrade pip
	${VENV} pip3 install wheel
	${VENV} pip3 install -r requirements.txt

create_venv:
	python3 -m venv .venv

