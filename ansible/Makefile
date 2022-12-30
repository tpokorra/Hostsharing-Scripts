PYTHON_VERSION := 3.10.9

help:
	@echo
	@echo "Neueres Python installieren, ggfs. auch Ansible"
	@echo "  make install_ansible"
	@echo "  make install_python"

install_python:
	mkdir -p ${HOME}/opt
	mkdir -p ${HOME}/build
	cd ${HOME}/build; wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
	cd ${HOME}/build; tar xzf Python-${PYTHON_VERSION}.tgz
	cd ${HOME}/build/Python-${PYTHON_VERSION}; ./configure --enable-optimizations --prefix=${HOME}/opt; make; make install
	rm -rf ${HOME}/build
	echo 'export PATH=$$HOME/opt/bin:$$HOME/.local/bin:$$PATH' >> ${HOME}/.profile

# Ansible requires Python >= 3.8; on Debian Buster we have Python 3.7.3
install_ansible: install_python
	echo "PIPENV_VENV_IN_PROJECT=1" >> ${HOME}/.profile
	. ${HOME}/.profile; python3 -m pip install --user --upgrade pip pipenv
	mkdir -p ${HOME}/ansible
	cd ${HOME}/ansible; . ${HOME}/.profile; pipenv install ansible

