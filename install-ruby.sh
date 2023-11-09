#!/bin/bash

# see https://www.ruby-lang.org/en/downloads/releases/
export version=3.1.4

git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
source ~/.bash_profile

rbenv install $version
rbenv global $version
gem install bundler
rbenv rehash

source ~/.bash_profile
ruby -v