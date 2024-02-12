#!/bin/bash

mkdir -p ~/bin
cd ~/bin

# see https://getcomposer.org/download/
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
checksum=edb40769019ccf227279e3bdd1f5b2e9950eb000c3233ee85148944e555d97be3ea4f40c3c2fe73b22f875385f6a5155
php -r "if (hash_file('sha384', 'composer-setup.php') === '$checksum') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"

cat > composer <<FINISH
#!/bin/bash
~/bin/composer.phar  "\$@"
FINISH

chmod a+x composer
chmod a+x composer.phar

line='export PATH=$HOME/bin:$PATH'
grep -qxF "$line" ~/.profile || echo $line >> ~/.profile
chmod a+x ~/.profile

source ~/.profile
composer --version
