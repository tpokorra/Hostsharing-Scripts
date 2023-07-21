#!/bin/bash

PAC=`id -nu`
cd ~/users
for u in *; do sudo -u $PAC-$u /bin/bash -c "whoami && source ~/.profile && systemctl --user restart nginx"; done
