#!/bin/bash

mkdir -p ~/bin
cd ~/bin

# see https://phpunit.de/documentation.html
version=9
wget -O phpunit.phar https://phar.phpunit.de/phpunit-$version.phar


cat > phpunit <<FINISH
#!/bin/bash
~/bin/phpunit.phar "\$@"
FINISH

chmod a+x phpunit
chmod a+x phpunit.phar

line='export PATH=$HOME/bin:$PATH'
grep -qxF "$line" ~/.profile || echo $line >> ~/.profile
chmod a+x ~/.profile

source ~/.profile
phpunit --version
