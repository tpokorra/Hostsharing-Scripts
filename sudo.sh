#!/bin/bash

PAC=`id -nu`

if ! [ -d ~/users ]; then
    echo "kein ~/users Verzeichnis vorhanden - Abbruch"
    exit 0
fi

if [ -z $1 ]; then
    echo "Aufruf: ~/bin/sudo.sh mustermann"
    echo "   um in den Benutzer $PAC-mustermann zu wechseln"
    exit 0
fi

username=$1

if [ ! -d $HOME/users/$username ]
then
    echo "Kann den Benutzer $username nicht finden"

    if [ ! -z "`ls $HOME/users -1 | grep $username`" ]
    then
      echo
      echo "Es gibt diese Benutzer, die ähnlich sind:"
      ls $HOME/users -1 | grep $username
    fi

    exit -1
fi

# if user has bash shell
# sudo -iu `whoami`"-$username"

# $HOME/.profile should have: cd ~
sudo -u `whoami`"-$username" bash --login
