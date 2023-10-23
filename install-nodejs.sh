#!/bin/bash

mkdir -p ~/bin
cd ~/bin

# see https://nodejs.org/de/download
version=18

touch ~/.profile
chmod u+x ~/.profile
cd /tmp
# see https://github.com/nvm-sh/nvm/releases
wget https://raw.githubusercontent.com/creationix/nvm/v0.39.5/install.sh
chmod u+x install.sh
./install.sh
rm ./install.sh

source ~/.profile
nvm install $version
nvm alias default $version

source ~/.profile
node --version
npm --version
