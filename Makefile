VENV := . .venv/bin/activate &&

all:
	@echo "help:"
	@echo "  make init"

init: create_venv pip_packages copy_scripts

pip_packages:
	${VENV} pip3 install --upgrade pip
	${VENV} pip3 install wheel
	${VENV} pip3 install -r requirements.txt

create_venv:
	python3 -m venv .venv

copy_scripts:
	PAC=`id -nu` && for f in *.py; do cat $$f | sed -e "s/xyz00/$$PAC/g" > $${f%.*}; chmod a+x $${f%.*}; done
