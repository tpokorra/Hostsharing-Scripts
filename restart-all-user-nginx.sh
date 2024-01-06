#!/bin/bash

PAC=`id -nu`
cd ~/users
for u in *; do sudo -u $PAC-$u /bin/bash -c "if [ -f ~/.config/systemd/user/nginx.service ]; then whoami && source ~/.profile && systemctl --user restart nginx; fi"; done
